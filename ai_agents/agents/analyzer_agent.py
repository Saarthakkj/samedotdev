from config.system_config import SystemConfig
from pathlib import Path
import logging
import json
from typing import Dict, Optional, List, Tuple
import os
import asyncio
import cv2
import numpy as np
from collections import Counter
import google.generativeai as genai
import aiohttp
from firecrawl import FirecrawlApp
import base64
import re

class AnalyzerAgent:
    """Unified agent for website crawling, screenshot capture, and comprehensive UI analysis using Firecrawl and Gemini."""
    
    def __init__(self, config: SystemConfig, name: str = "AnalyzerAgent"):
        self.name = name
        self.config = config
        self.logger = self._setup_logger()
        
        # Initialize Gemini API
        if not hasattr(config, 'gemini_api_key') or not config.gemini_api_key:
            raise ValueError("Gemini API key is required for analysis")
        genai.configure(api_key=config.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Initialize Firecrawl
        if not hasattr(config, 'firecrawl_api_key') or not config.firecrawl_api_key:
            raise ValueError("Firecrawl API key is required for crawling")
        self.firecrawl = FirecrawlApp(api_key=config.firecrawl_api_key)
        
        self.logger.info("Initialized AnalyzerAgent with Gemini and Firecrawl")

    def _setup_logger(self):
        """Setup logger for the agent."""
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        return logging.getLogger(self.__class__.__name__)

    def _extract_dominant_colors(self, image: np.ndarray, num_colors: int = 10) -> List[Tuple[str, float]]:
        """Extract dominant colors from image using K-means clustering."""
        try:
            from sklearn.cluster import KMeans
            pixels = image.reshape(-1, 3)
            mask = ~((pixels == [0, 0, 0]).all(axis=1) | (pixels == [255, 255, 255]).all(axis=1))
            filtered_pixels = pixels[mask]
            
            if len(filtered_pixels) == 0:
                return []
            
            if len(filtered_pixels) > 10000:
                indices = np.random.choice(len(filtered_pixels), 10000, replace=False)
                sample_pixels = filtered_pixels[indices]
            else:
                sample_pixels = filtered_pixels
            
            kmeans = KMeans(n_clusters=min(num_colors, len(sample_pixels)), random_state=42, n_init=10)
            kmeans.fit(sample_pixels)
            
            colors = kmeans.cluster_centers_.astype(int)
            labels = kmeans.labels_
            label_counts = Counter(labels)
            total_pixels = len(labels)
            
            color_info = [
                ("#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2]), (label_counts[i] / total_pixels) * 100)
                for i, color in enumerate(colors)
            ]
            color_info.sort(key=lambda x: x[1], reverse=True)
            return color_info
            
        except Exception as e:
            self.logger.error(f"Error extracting dominant colors: {e}")
            return []

    def _analyze_color_scheme(self, dominant_colors: List[Tuple[str, float]]) -> Dict:
        """Analyze the color scheme and categorize colors."""
        if not dominant_colors:
            return {}
        
        return {
            "primary_color": dominant_colors[0][0] if dominant_colors else None,
            "secondary_colors": [color[0] for color in dominant_colors[1:4]],
            "accent_colors": [color[0] for color in dominant_colors[4:7]],
            "color_distribution": {color[0]: f"{color[1]:.1f}%" for color in dominant_colors},
            "theme_analysis": self._detect_theme_type(dominant_colors)
        }

    def _detect_theme_type(self, dominant_colors: List[Tuple[str, float]]) -> str:
        """Detect if the theme is light, dark, or mixed based on dominant colors."""
        if not dominant_colors:
            return "unknown"
        
        light_colors = sum(percentage for hex_color, percentage in dominant_colors[:5]
                          if sum(int(hex_color.lstrip('#')[i:i+2], 16) * w for i, w in [(0, 0.299), (2, 0.587), (4, 0.114)]) > 128)
        dark_colors = sum(percentage for _, percentage in dominant_colors[:5]) - light_colors
        
        if light_colors > dark_colors * 2:
            return "light"
        elif dark_colors > light_colors * 2:
            return "dark"
        return "mixed"

    def _divide_image_into_segments(self, image: np.ndarray) -> List[Dict]:
        """Divide image into logical segments with overlap for context preservation."""
        height, width = image.shape[:2]
        segments = []
        
        # Define segment strategy based on image dimensions
        if width > 1920 or height > 1080:
            h_segments, w_segments = 3, 3
        elif width > 1200 or height > 800:
            h_segments, w_segments = 2, 3
        else:
            h_segments, w_segments = 2, 2
        
        segment_height = height // h_segments
        segment_width = width // w_segments
        overlap_h = int(segment_height * 0.2)
        overlap_w = int(segment_width * 0.2)
        
        segment_id = 0
        for i in range(h_segments):
            for j in range(w_segments):
                y_start = max(0, i * segment_height - overlap_h)
                y_end = min(height, (i + 1) * segment_height + overlap_h)
                x_start = max(0, j * segment_width - overlap_w)
                x_end = min(width, (j + 1) * segment_width + overlap_w)
                
                segment_image = image[y_start:y_end, x_start:x_end]
                position = self._determine_segment_position(i, j, h_segments, w_segments)
                
                segments.append({
                    "id": segment_id,
                    "image": segment_image,
                    "coordinates": (x_start, y_start, x_end, y_end),
                    "position": position,
                    "dimensions": (x_end - x_start, y_end - y_start)
                })
                segment_id += 1
        
        self.logger.info(f"Divided image into {len(segments)} segments")
        return segments

    def _determine_segment_position(self, row: int, col: int, total_rows: int, total_cols: int) -> str:
        """Determine the logical position of a segment in the layout."""
        if total_rows == 1 and total_cols == 1:
            return "full"
        elif total_rows == 1:
            if col == 0:
                return "left"
            elif col == total_cols - 1:
                return "right"
            else:
                return "center"
        elif total_cols == 1:
            if row == 0:
                return "top"
            elif row == total_rows - 1:
                return "bottom"
            else:
                return "center"
        else:
            position_parts = []
            if row == 0:
                position_parts.append("top")
            elif row == total_rows - 1:
                position_parts.append("bottom")
            else:
                position_parts.append("middle")
                
            if col == 0:
                position_parts.append("left")
            elif col == total_cols - 1:
                position_parts.append("right")
            else:
                position_parts.append("center")
                
            return "_".join(position_parts)

    def _extract_json_from_response(self, response_text: str) -> Dict:
        """Extract JSON from Gemini response text, handling various formats."""
        if not response_text or not response_text.strip():
            return {}
        
        # Try to parse as direct JSON first
        try:
            return json.loads(response_text.strip())
        except json.JSONDecodeError:
            pass
        
        # Look for JSON blocks in markdown format
        json_patterns = [
            r'```json\s*(\{.*?\})\s*```',
            r'```\s*(\{.*?\})\s*```',
            r'(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})'
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, response_text, re.DOTALL | re.IGNORECASE)
            for match in matches:
                try:
                    return json.loads(match.strip())
                except json.JSONDecodeError:
                    continue
        
        # If no valid JSON found, create structured response from text
        return self._create_structured_response_from_text(response_text)

    def _create_structured_response_from_text(self, text: str) -> Dict:
        """Create a structured response from unstructured text."""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        return {
            "segment_info": {
                "position": "unknown",
                "coordinates": [0, 0, 0, 0],
                "primary_role": "content_area",
                "segment_type": "ui_section"
            },
            "discovered_elements": {
                "text_content": [line for line in lines[:5] if not line.startswith('{') and not line.startswith('[')],
                "interactive_elements": ["buttons", "links", "forms"],
                "visual_elements": ["images", "icons", "graphics"],
                "layout_structure": "hierarchical"
            },
            "component_identification": {
                "primary_components": ["container", "content", "navigation"]
            },
            "segment_colors": {
                "dominant_colors": ["#ffffff", "#000000"],
                "color_usage": "standard"
            },
            "implementation_specs": {
                "required_components": ["div", "section", "article"],
                "css_requirements": ["flexbox", "grid", "responsive"],
                "responsive_considerations": ["mobile-first", "breakpoints"],
                "dependencies": ["none"]
            },
            "integration_notes": {
                "connections_to_other_segments": "adjacent",
                "shared_elements": "header_footer",
                "z_index_considerations": "standard"
            },
            "raw_analysis": text[:500] if text else "No analysis available"
        }

    async def _analyze_segment(self, segment: Dict, global_colors: List[Tuple[str, float]], segment_index: int, total_segments: int) -> Dict:
        """Analyze individual segment with Gemini vision model."""
        segment_image = segment["image"]
        position = segment["position"]
        coordinates = segment["coordinates"]
        
        try:
            _, img_encoded = cv2.imencode('.png', segment_image, [cv2.IMWRITE_PNG_COMPRESSION, 0])
            img_bytes = img_encoded.tobytes()
            
            segment_colors = self._extract_dominant_colors(segment_image, num_colors=8)
            segment_colors_str = ", ".join([f"{color[0]} ({percentage:.1f}%)" for color, percentage in segment_colors[:5]])
            global_colors_str = ", ".join([f"{color[0]} ({percentage:.1f}%)" for color, percentage in global_colors[:8]])
            
            prompt = f"""
            Analyze this UI segment {segment_index + 1} of {total_segments} located at {position} position.
            
            Context:
            - Segment coordinates: {coordinates}
            - Global dominant colors: {global_colors_str}
            - Segment specific colors: {segment_colors_str}
            
            Please provide a detailed analysis in JSON format with these exact keys:
            {{
                "segment_info": {{
                    "position": "{position}",
                    "coordinates": {list(coordinates)},
                    "primary_role": "describe main purpose",
                    "segment_type": "header/navigation/content/sidebar/footer"
                }},
                "discovered_elements": {{
                    "text_content": ["list of text elements found"],
                    "interactive_elements": ["buttons, links, forms, etc"],
                    "visual_elements": ["images, icons, graphics"],
                    "layout_structure": "describe layout type"
                }},
                "component_identification": {{
                    "primary_components": ["main UI components identified"]
                }},
                "segment_colors": {{
                    "dominant_colors": ["color hex codes"],
                    "color_usage": "describe how colors are used"
                }},
                "implementation_specs": {{
                    "required_components": ["HTML elements needed"],
                    "css_requirements": ["CSS features required"],
                    "responsive_considerations": ["mobile/tablet considerations"],
                    "dependencies": ["external libraries if any"]
                }},
                "integration_notes": {{
                    "connections_to_other_segments": "how it connects",
                    "shared_elements": "common elements",
                    "z_index_considerations": "layering notes"
                }}
            }}
            
            Focus on visible UI elements, their purpose, and implementation requirements.
            """
            
            response = await self.model.generate_content_async([prompt, {"mime_type": "image/png", "data": img_bytes}])
            
            if not response or not response.text:
                self.logger.warning(f"Empty response for segment {segment_index}")
                analysis = self._create_structured_response_from_text("Empty response from Gemini")
            else:
                analysis = self._extract_json_from_response(response.text)
            
            # Ensure required structure exists
            analysis.setdefault("segment_info", {}).update({
                "position": position,
                "coordinates": coordinates
            })
            
            analysis["segment_metadata"] = {
                "segment_id": segment["id"],
                "position": position,
                "coordinates": coordinates,
                "dimensions": segment["dimensions"],
                "analysis_timestamp": asyncio.get_event_loop().time(),
                "success": True
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Segment {segment_index} analysis failed: {e}")
            return {
                "segment_info": {
                    "position": position,
                    "coordinates": coordinates,
                    "primary_role": "unknown",
                    "segment_type": "error",
                    "error": str(e)
                },
                "discovered_elements": {
                    "text_content": [],
                    "interactive_elements": [],
                    "visual_elements": [],
                    "layout_structure": "unknown"
                },
                "component_identification": {"primary_components": []},
                "segment_colors": {"dominant_colors": [], "color_usage": "unknown"},
                "implementation_specs": {
                    "required_components": [],
                    "css_requirements": [],
                    "responsive_considerations": [],
                    "dependencies": []
                },
                "integration_notes": {
                    "connections_to_other_segments": "unknown",
                    "shared_elements": "unknown",
                    "z_index_considerations": "unknown"
                },
                "segment_metadata": {
                    "error": True,
                    "segment_id": segment["id"],
                    "position": position,
                    "coordinates": coordinates,
                    "error_message": str(e)
                }
            }

    async def _combine_segment_analyses(self, segment_analyses: List[Dict], global_context: Dict) -> Dict:
        """Combine segment analyses into a unified analysis."""
        successful_analyses = [a for a in segment_analyses if not a.get("segment_metadata", {}).get("error")]
        
        if not successful_analyses:
            self.logger.warning("No successful segment analyses to combine")
            return {
                "unified_analysis": {
                    "interface_type": "unknown",
                    "overall_purpose": "Could not determine due to analysis failures",
                    "layout_strategy": "unknown",
                    "design_system": "unknown"
                },
                "component_architecture": {
                    "layout_components": [],
                    "feature_components": [],
                    "ui_components": []
                },
                "implementation_guide": {
                    "project_structure": "standard_web_project",
                    "development_priorities": ["error_handling", "debugging"],
                    "responsive_breakpoints": ["768px", "1024px", "1200px"],
                    "technical_requirements": ["modern_browser_support"]
                },
                "recreation_specifications": {
                    "html_structure": "basic_html5_structure",
                    "css_architecture": "component_based",
                    "javascript_functionality": "minimal",
                    "accessibility_requirements": ["wcag_aa"],
                    "performance_considerations": ["optimization"],
                    "browser_compatibility": ["modern_browsers"]
                },
                "quality_assurance": {
                    "component_checklist": ["basic_validation"],
                    "responsive_testing": ["mobile", "tablet", "desktop"],
                    "interaction_testing": ["click", "hover", "focus"],
                    "visual_regression": ["screenshot_comparison"]
                },
                "analysis_metadata": {
                    "segments_processed": len(segment_analyses),
                    "successful_segments": len(successful_analyses),
                    "combination_timestamp": asyncio.get_event_loop().time(),
                    "analysis_quality": "poor"
                }
            }
        
        # Create summaries for the combination prompt
        segments_summary = []
        all_components = []
        all_colors = set()
        
        for i, analysis in enumerate(successful_analyses):
            segment_info = analysis.get("segment_info", {})
            components = analysis.get("component_identification", {}).get("primary_components", [])
            colors = analysis.get("segment_colors", {}).get("dominant_colors", [])
            
            segments_summary.append(f"Segment {i+1} ({segment_info.get('position', 'unknown')}): {segment_info.get('primary_role', 'Unknown role')}")
            all_components.extend(components)
            all_colors.update(colors)
        
        prompt = f"""
        Combine the following segment analyses into a unified UI analysis:
        
        Segments analyzed:
        {chr(10).join(segments_summary)}
        
        Global context: {json.dumps(global_context, indent=2)}
        
        All identified components: {list(set(all_components))}
        All colors found: {list(all_colors)}
        
        Please provide a comprehensive analysis in JSON format with these exact keys:
        {{
            "unified_analysis": {{
                "interface_type": "web_application/landing_page/dashboard/etc",
                "overall_purpose": "main purpose of the interface",
                "layout_strategy": "grid/flexbox/traditional/etc",
                "design_system": "modern/classic/minimal/etc"
            }},
            "component_architecture": {{
                "layout_components": ["main structural components"],
                "feature_components": ["functional components"],
                "ui_components": ["interface elements"]
            }},
            "implementation_guide": {{
                "project_structure": "recommended folder structure",
                "development_priorities": ["ordered list of priorities"],
                "responsive_breakpoints": ["breakpoint values"],
                "technical_requirements": ["required technologies"]
            }},
            "recreation_specifications": {{
                "html_structure": "HTML architecture approach",
                "css_architecture": "CSS organization method",
                "javascript_functionality": "JS requirements",
                "accessibility_requirements": ["a11y standards"],
                "performance_considerations": ["optimization strategies"],
                "browser_compatibility": ["supported browsers"]
            }},
            "quality_assurance": {{
                "component_checklist": ["testing checklist items"],
                "responsive_testing": ["testing scenarios"],
                "interaction_testing": ["interaction types to test"],
                "visual_regression": ["visual testing approaches"]
            }}
        }}
        
        Focus on creating actionable implementation guidance and cohesive component hierarchy.
        """
        
        try:
            response = await self.model.generate_content_async([prompt])
            
            if not response or not response.text:
                self.logger.warning("Empty response from unified analysis")
                unified_analysis = self._create_fallback_unified_analysis(successful_analyses, global_context)
            else:
                unified_analysis = self._extract_json_from_response(response.text)
                
                # Ensure required structure
                unified_analysis.setdefault("unified_analysis", {})
                unified_analysis.setdefault("component_architecture", {})
                unified_analysis.setdefault("implementation_guide", {})
                unified_analysis.setdefault("recreation_specifications", {})
                unified_analysis.setdefault("quality_assurance", {})
            
            unified_analysis["analysis_metadata"] = {
                "segments_processed": len(segment_analyses),
                "successful_segments": len(successful_analyses),
                "combination_timestamp": asyncio.get_event_loop().time(),
                "analysis_quality": "good" if len(successful_analyses) > len(segment_analyses) * 0.7 else "moderate"
            }
            
            return unified_analysis
            
        except Exception as e:
            self.logger.error(f"Failed to combine analyses: {e}")
            return self._create_fallback_unified_analysis(successful_analyses, global_context)

    def _create_fallback_unified_analysis(self, successful_analyses: List[Dict], global_context: Dict) -> Dict:
        """Create a fallback unified analysis when Gemini fails."""
        all_components = []
        layout_types = []
        
        for analysis in successful_analyses:
            components = analysis.get("component_identification", {}).get("primary_components", [])
            all_components.extend(components)
            
            segment_info = analysis.get("segment_info", {})
            if segment_info.get("segment_type"):
                layout_types.append(segment_info["segment_type"])
        
        return {
            "unified_analysis": {
                "interface_type": "web_interface",
                "overall_purpose": "User interface with multiple functional areas",
                "layout_strategy": "multi_section_layout",
                "design_system": global_context.get("theme_analysis", "modern")
            },
            "component_architecture": {
                "layout_components": list(set(["container", "section", "header", "footer"])),
                "feature_components": list(set(all_components[:10])),
                "ui_components": list(set(["button", "link", "text", "image"]))
            },
            "implementation_guide": {
                "project_structure": "modular_component_structure",
                "development_priorities": ["responsive_design", "accessibility", "performance"],
                "responsive_breakpoints": ["768px", "1024px", "1200px"],
                "technical_requirements": ["html5", "css3", "javascript"]
            },
            "recreation_specifications": {
                "html_structure": "semantic_html5",
                "css_architecture": "component_based_css",
                "javascript_functionality": "progressive_enhancement",
                "accessibility_requirements": ["semantic_markup", "keyboard_navigation", "screen_reader_support"],
                "performance_considerations": ["image_optimization", "css_minification", "lazy_loading"],
                "browser_compatibility": ["modern_browsers", "ie11_fallback"]
            },
            "quality_assurance": {
                "component_checklist": ["html_validation", "css_validation", "js_linting"],
                "responsive_testing": ["mobile", "tablet", "desktop", "large_screen"],
                "interaction_testing": ["click_events", "hover_states", "focus_management"],
                "visual_regression": ["cross_browser_testing", "screenshot_comparison"]
            },
            "analysis_metadata": {
                "segments_processed": len(successful_analyses),
                "successful_segments": len(successful_analyses),
                "combination_timestamp": asyncio.get_event_loop().time(),
                "analysis_quality": "fallback",
                "fallback_reason": "gemini_combination_failed"
            }
        }

    async def capture_screenshot(self, url: str, output_path: str = None, options: Dict = None) -> str:
        """Capture full-page screenshot using Firecrawl v1 API."""
        output_path = output_path or "screenshots/fullpage_screenshot.png"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        options = options or {"waitFor": 5000, "timeout": 60000}  # Increased wait time and timeout
        
        try:
            # Log the request parameters
            self.logger.debug(f"Calling scrape_url with url={url}, formats=['screenshot@fullPage'], "
                            f"actions=[wait: {options['waitFor']}ms, screenshot], timeout={options['timeout']}")
            
            # Call Firecrawl scrape_url with direct keyword arguments
            scrape_result = self.firecrawl.scrape_url(
                url=url,
                formats=["screenshot@fullPage"],
                actions=[
                    {"type": "wait", "milliseconds": options["waitFor"]},
                    {"type": "screenshot"}
                ],
                timeout=options["timeout"]
            )
            
            # Log the full response
            self.logger.debug(f"Scrape result: {json.dumps(vars(scrape_result) if hasattr(scrape_result, '__dict__') else scrape_result, default=str)}")
            
            # Handle ScrapeResponse object or dictionary
            if hasattr(scrape_result, 'success'):
                if not scrape_result.success:
                    raise Exception(f"Failed to capture screenshot: {getattr(scrape_result, 'error', 'Unknown error')}")
                screenshot_data = (
                    getattr(scrape_result, 'screenshot', None) or
                    (scrape_result.data.get('screenshot') if hasattr(scrape_result, 'data') else None) or
                    (scrape_result.data.get('actions', {}).get('screenshots', [None])[0] if hasattr(scrape_result, 'data') else None)
                )
            else:
                if not scrape_result.get('success', False):
                    raise Exception(f"Failed to capture screenshot: {scrape_result.get('error', 'Unknown error')}")
                screenshot_data = (
                    scrape_result.get('data', {}).get('screenshot') or
                    scrape_result.get('data', {}).get('actions', {}).get('screenshots', [None])[0]
                )
            
            if not screenshot_data:
                raise Exception("No screenshot data returned from Firecrawl")
            
            # Log screenshot data type and preview
            self.logger.debug(f"Screenshot data type: {type(screenshot_data)}, preview: {str(screenshot_data)[:100]}")
            
            # Handle base64 encoded screenshot or URL
            if isinstance(screenshot_data, str) and screenshot_data.startswith("data:image"):
                screenshot_data = base64.b64decode(screenshot_data.split(',')[1])
            elif isinstance(screenshot_data, str) and screenshot_data.startswith("http"):
                async with aiohttp.ClientSession() as session:
                    async with session.get(screenshot_data) as response:
                        if response.status != 200:
                            raise Exception(f"Failed to fetch screenshot from URL: {response.status}")
                        screenshot_data = await response.read()
            else:
                raise Exception(f"Unexpected screenshot data format: {type(screenshot_data)}")
            
            # Save screenshot to file
            with open(output_path, 'wb') as f:
                f.write(screenshot_data)
            
            self.logger.info(f"Screenshot saved to {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Screenshot capture failed: {e}")
            raise
    
    async def extract_urls(self, url: str, limit: int = 100) -> List[str]:
        """Extract all URLs from a website using Firecrawl's map endpoint."""
        try:
            # Use correct v1 API format for map with keyword arguments
            map_result = self.firecrawl.map_url(url, limit=limit)
            
            if not map_result.get('success', False):
                raise Exception(f"Failed to map URLs: {map_result.get('error', 'Unknown error')}")
            
            urls = map_result.get('urls', [])
            self.logger.info(f"Extracted {len(urls)} URLs from {url}")
            return urls
        except Exception as e:
            self.logger.error(f"Failed to extract URLs: {e}")
            return []

    async def analyze_screenshot(self, image_path: str, html_content: str = "") -> Dict:
        """Analyze screenshot using divide-and-conquer strategy and Gemini."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width = image_rgb.shape[:2]
        
        dominant_colors = self._extract_dominant_colors(image_rgb, num_colors=15)
        color_analysis = self._analyze_color_scheme(dominant_colors)
        
        segments = self._divide_image_into_segments(image_rgb)
        segment_analyses = await asyncio.gather(*[
            self._analyze_segment(segment, dominant_colors, i, len(segments))
            for i, segment in enumerate(segments)
        ])
        
        global_context = {
            "dimensions": (width, height),
            "theme_analysis": color_analysis.get("theme_analysis", "unknown"),
            "total_segments": len(segments),
            "dominant_colors": dominant_colors,
            "html_context": html_content[:500] if html_content else None
        }
        
        unified_analysis = await self._combine_segment_analyses(segment_analyses, global_context)
        unified_analysis["global_analysis"] = {
            "image_metadata": {"dimensions": (width, height), "aspect_ratio": round(width / height, 2)},
            "color_analysis": color_analysis,
            "dominant_colors_detailed": dominant_colors,
            "segmentation_strategy": {"total_segments": len(segments), "segment_positions": [seg["position"] for seg in segments]}
        }
        
        return unified_analysis

    async def analyze_website(self, url: str, output_path: str = "screenshots/fullpage_screenshot.png", crawl_limit: int = 100) -> Dict:
        """Crawl website, capture screenshot, and analyze UI comprehensively."""
        try:
            # Capture screenshot
            screenshot_path = await self.capture_screenshot(url, output_path)
            
            # Crawl website for HTML and URLs using correct v1 API
            crawl_result = self.firecrawl.crawl_url(
                url,
                limit=crawl_limit,
                formats=["markdown", "html"]
            )
            
            html_content = ""
            if crawl_result.get('success', False):
                crawl_data = crawl_result.get('data', [])
                html_content = "\n".join([page.get("html", "") for page in crawl_data if isinstance(page, dict)])
            
            # Extract URLs
            urls = await self.extract_urls(url, crawl_limit)
            
            # Analyze screenshot
            analysis = await self.analyze_screenshot(screenshot_path, html_content)
            analysis["website_metadata"] = {
                "url": url,
                "crawled_urls": urls,
                "crawl_timestamp": asyncio.get_event_loop().time(),
                "screenshot_path": screenshot_path
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Website analysis failed: {e}")
            raise