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
from google.adk.artifacts import InMemoryArtifactService
import google.generativeai as genai

class DCGenAnalyzer:
    """DCGen-enhanced analyzer implementing comprehensive screenshot analysis using Google ADK"""
    
    def __init__(self, config: SystemConfig, name: str = "DCGenAnalyzer"):
        self.name = name
        self.config = config
        self.logger = self._setup_logger()
        self.artifact_service = InMemoryArtifactService()
        
        # Initialize Gemini API
        if not hasattr(config, 'gemini_api_key') or not config.gemini_api_key:
            raise ValueError("Gemini API key is required for analysis")
        
        self.logger.info("Initializing Gemini API for comprehensive screenshot analysis")
        genai.configure(api_key=config.gemini_api_key)
        self.model = self._initialize_gemini_model()
        
        if not self.model:
            raise RuntimeError("Failed to initialize Gemini model")

    def _setup_logger(self):
        """Setup logger for the analyzer"""
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(self.__class__.__name__)

    def _initialize_gemini_model(self):
        """Initialize Gemini model with fallback options"""
        model_options = [
            'gemini-2.0-flash-exp',
            'gemini-2.0-flash', 
            'gemini-1.5-pro',
            'gemini-pro-vision',
            'gemini-pro'
        ]
        
        for model_name in model_options:
            try:
                model = genai.GenerativeModel(model_name)
                self.logger.info(f"Successfully initialized {model_name} model")
                return model
            except Exception as e:
                self.logger.warning(f"Failed to initialize {model_name}: {e}")
                continue
        
        self.logger.error("Failed to initialize any Gemini model")
        return None

    def _extract_dominant_colors(self, image: np.ndarray, num_colors: int = 10) -> List[Tuple[str, float]]:
        """
        Extract dominant colors from image using K-means clustering
        
        Args:
            image: RGB image array
            num_colors: Number of dominant colors to extract
            
        Returns:
            List of (hex_color, percentage) tuples
        """
        try:
            # Reshape image to be a list of pixels
            pixels = image.reshape(-1, 3)
            
            # Remove pure black and white pixels to avoid noise
            mask = ~((pixels == [0, 0, 0]).all(axis=1) | (pixels == [255, 255, 255]).all(axis=1))
            filtered_pixels = pixels[mask]
            
            if len(filtered_pixels) == 0:
                return []
            
            # Use K-means to find dominant colors
            from sklearn.cluster import KMeans
            
            # Limit number of pixels for performance
            if len(filtered_pixels) > 10000:
                indices = np.random.choice(len(filtered_pixels), 10000, replace=False)
                sample_pixels = filtered_pixels[indices]
            else:
                sample_pixels = filtered_pixels
            
            kmeans = KMeans(n_clusters=min(num_colors, len(sample_pixels)), random_state=42, n_init=10)
            kmeans.fit(sample_pixels)
            
            # Get colors and their frequencies
            colors = kmeans.cluster_centers_.astype(int)
            labels = kmeans.labels_
            
            # Calculate percentages
            label_counts = Counter(labels)
            total_pixels = len(labels)
            
            color_info = []
            for i, color in enumerate(colors):
                percentage = (label_counts[i] / total_pixels) * 100
                hex_color = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
                color_info.append((hex_color, percentage))
            
            # Sort by percentage (most dominant first)
            color_info.sort(key=lambda x: x[1], reverse=True)
            
            return color_info
            
        except ImportError:
            self.logger.warning("sklearn not available, using basic color extraction")
            return self._extract_colors_basic(image, num_colors)
        except Exception as e:
            self.logger.error(f"Error extracting dominant colors: {e}")
            return self._extract_colors_basic(image, num_colors)

    def _extract_colors_basic(self, image: np.ndarray, num_colors: int = 10) -> List[Tuple[str, float]]:
        """
        Basic color extraction without sklearn
        """
        try:
            # Get unique colors and their counts
            pixels = image.reshape(-1, 3)
            unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
            
            # Sort by frequency
            sorted_indices = np.argsort(counts)[::-1]
            top_colors = unique_colors[sorted_indices[:num_colors]]
            top_counts = counts[sorted_indices[:num_colors]]
            
            total_pixels = len(pixels)
            color_info = []
            
            for color, count in zip(top_colors, top_counts):
                percentage = (count / total_pixels) * 100
                hex_color = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
                color_info.append((hex_color, percentage))
            
            return color_info
            
        except Exception as e:
            self.logger.error(f"Error in basic color extraction: {e}")
            return []

    def _analyze_color_scheme(self, dominant_colors: List[Tuple[str, float]]) -> Dict:
        """
        Analyze the color scheme and categorize colors
        """
        if not dominant_colors:
            return {}
        
        color_analysis = {
            "primary_color": dominant_colors[0][0] if dominant_colors else None,
            "secondary_colors": [color[0] for color in dominant_colors[1:4]],
            "accent_colors": [color[0] for color in dominant_colors[4:7]],
            "color_distribution": {color[0]: f"{color[1]:.1f}%" for color in dominant_colors},
            "theme_analysis": self._detect_theme_type(dominant_colors)
        }
        
        return color_analysis

    def _detect_theme_type(self, dominant_colors: List[Tuple[str, float]]) -> str:
        """
        Detect if the theme is light, dark, or mixed based on dominant colors
        """
        if not dominant_colors:
            return "unknown"
        
        light_colors = 0
        dark_colors = 0
        
        for hex_color, percentage in dominant_colors[:5]:  # Check top 5 colors
            # Convert hex to RGB
            hex_color = hex_color.lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            
            # Calculate brightness
            brightness = (r * 0.299 + g * 0.587 + b * 0.114)
            
            if brightness > 128:
                light_colors += percentage
            else:
                dark_colors += percentage
        
        if light_colors > dark_colors * 2:
            return "light"
        elif dark_colors > light_colors * 2:
            return "dark"
        else:
            return "mixed"

    async def analyze_screenshot_dcgen(self, image_path: str, html_content: str = "") -> Dict:
        """
        Main comprehensive screenshot analysis method using AI with improved color detection
        
        Args:
            image_path: Path to screenshot
            html_content: Optional HTML content
        
        Returns:
            Complete comprehensive analysis
        """
        self.logger.info(f"Starting comprehensive analysis for image: {image_path}")
        
        # Validate image file
        if not os.path.exists(image_path):
            self.logger.error(f"Image file not found: {image_path}")
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Load and prepare image with better color preservation
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Convert BGR to RGB for proper color analysis
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width = image_rgb.shape[:2]
        
        self.logger.info(f"Image loaded: {width}x{height} pixels")
        
        # Extract dominant colors before sending to AI
        self.logger.info("Extracting dominant colors...")
        dominant_colors = self._extract_dominant_colors(image_rgb, num_colors=12)
        color_analysis = self._analyze_color_scheme(dominant_colors)
        
        # Log detected colors for debugging
        self.logger.info(f"Detected dominant colors: {[color[0] for color in dominant_colors[:5]]}")
        
        # Convert to high-quality PNG bytes for AI analysis
        # Use maximum quality to preserve colors
        encode_params = [cv2.IMWRITE_PNG_COMPRESSION, 0]  # No compression
        _, img_encoded = cv2.imencode('.png', image, encode_params)
        img_bytes = img_encoded.tobytes()
        
        # Create comprehensive analysis prompt with pre-extracted color information
        detected_colors_str = ", ".join([f"{color[0]} ({percentage:.1f}%)" for color, percentage in dominant_colors[:8]])
        
        prompt = f"""
        You are an expert web designer and developer. Analyze this screenshot completely and provide a detailed JSON analysis of EVERYTHING you see.

        IMPORTANT COLOR GUIDANCE:
        I have pre-analyzed the image and detected these dominant colors: {detected_colors_str}
        The primary theme appears to be: {color_analysis.get('theme_analysis', 'unknown')}
        
        Please use these ACTUAL detected colors in your analysis rather than making assumptions. These colors were extracted using computer vision techniques for accuracy.

        DO NOT make assumptions about what components should be present. Instead, carefully examine the screenshot and dynamically identify and describe whatever components, sections, and elements you actually observe.

        COMPREHENSIVE ANALYSIS INSTRUCTIONS:

        1. **DISCOVER & EXTRACT EVERYTHING**:
           - Look at the screenshot carefully and identify what's actually there
           - Extract ALL visible text content word-for-word
           - Use the pre-detected colors I provided above - these are the ACTUAL colors in the image
           - Analyze typography (fonts, sizes, weights, styling) as you observe them
           - Describe the actual layout structure you see
           - Note the visual hierarchy and spacing patterns present
           - Identify the design style based on what you observe

        2. **DYNAMIC COMPONENT IDENTIFICATION**:
           - Examine the screenshot and identify what distinct components/sections are actually present
           - Don't assume standard web components - describe what you actually see
           - If there's a navigation area, describe it. If there isn't, don't mention it
           - If there are cards, forms, sidebars, modals, or any other elements, identify them based on visual observation
           - Create component names based on their actual function and appearance
           - Group related elements into logical components as you see them organized

        3. **COMPLETE CONTENT EXTRACTION**:
           - Extract every single piece of text visible in the image
           - Identify all interactive elements you can see (buttons, links, form fields, dropdowns, etc.)
           - Describe all images, icons, graphics, and visual elements present
           - Note any animations or interactive states that are visible

        4. **ACCURATE COLOR USAGE**:
           - Use ONLY the colors I detected and provided above
           - Don't invent or assume colors - stick to the detected palette
           - Describe how these actual colors are used throughout the interface
           - Note the color relationships and hierarchy

        Your response should be a JSON object that dynamically describes what you actually see. Use this flexible structure but adapt it based on your observations:

        {{
            "discovered_components": {{
                // Dynamically identify components based on what you see
            }},
            "visual_analysis": {{
                "all_colors_detected": {json.dumps([color[0] for color in dominant_colors])},
                "color_analysis": {json.dumps(color_analysis)},
                "typography_observed": {{
                    // Describe all fonts, sizes, weights you actually see
                }},
                "layout_structure": {{
                    // Describe the actual layout approach used
                }},
                "design_characteristics": {{
                    // Describe the design style you observe
                }}
            }},
            "content_extraction": {{
                "all_text_content": [
                    // Every piece of text visible, grouped logically
                ],
                "interactive_elements": [
                    // All buttons, links, form fields, etc. you can identify
                ],
                "media_elements": [
                    // All images, icons, graphics you can see
                ]
            }},
            "component_specifications": {{
                // For each component you identified, provide detailed specs
            }},
            "layout_relationships": {{
                // Describe how components relate to each other
            }},
            "implementation_requirements": {{
                "required_components": [],
                "styling_needs": [],
                "functionality_needs": [],
                "assets_needed": []
            }},
            "recreation_instructions": {{
                "component_breakdown": {{}},
                "styling_guide": {{}},
                "responsive_considerations": {{}}
            }}
        }}

        CRITICAL: 
        - Use ONLY the colors I provided from the computer vision analysis
        - Base everything on actual visual observation of the screenshot
        - Don't include components or elements you don't see
        - Don't use generic web template assumptions

        CONTEXT:
        - Image dimensions: {width}x{height} pixels
        - Pre-detected colors: {detected_colors_str}
        - Theme type: {color_analysis.get('theme_analysis', 'unknown')}
        - HTML content provided: {"Yes" if html_content else "No"}
        
        {f"HTML Context for reference: {html_content[:500]}..." if html_content else ""}
        """
        
        try:
            # Perform comprehensive AI analysis
            image_part = {"mime_type": "image/png", "data": img_bytes}
            response = await self.model.generate_content_async([prompt, image_part])
            
            if not response or not response.text:
                raise RuntimeError("Empty response from Gemini analysis")
            
            analysis = self._parse_gemini_response(response.text)
            
            # Ensure our detected colors are included in the final analysis
            if "visual_analysis" not in analysis:
                analysis["visual_analysis"] = {}
            
            analysis["visual_analysis"]["all_colors_detected"] = [color[0] for color in dominant_colors]
            analysis["visual_analysis"]["color_analysis"] = color_analysis
            analysis["visual_analysis"]["dominant_colors_with_percentages"] = dominant_colors
            
            self.logger.info("Comprehensive analysis completed successfully")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Failed to analyze screenshot: {e}")
            
            # Return a fallback analysis structure with detected colors
            return {
                "error": f"Analysis failed: {str(e)}",
                "discovered_components": {},
                "visual_analysis": {
                    "all_colors_detected": [color[0] for color in dominant_colors],
                    "color_analysis": color_analysis,
                    "dominant_colors_with_percentages": dominant_colors,
                    "typography_observed": {},
                    "layout_structure": {},
                    "design_characteristics": {}
                },
                "content_extraction": {
                    "all_text_content": [],
                    "interactive_elements": [],
                    "media_elements": []
                },
                "component_specifications": {},
                "layout_relationships": {},
                "implementation_requirements": {
                    "required_components": [],
                    "styling_needs": [],
                    "functionality_needs": [],
                    "assets_needed": []
                },
                "recreation_instructions": {
                    "component_breakdown": {},
                    "styling_guide": {},
                    "responsive_considerations": {}
                }
            }

    def _parse_gemini_response(self, response_text: str) -> Dict:
        """Parse Gemini response into structured analysis"""
        try:
            # Try to parse as JSON first
            try:
                analysis = json.loads(response_text)
            except json.JSONDecodeError:
                # Extract JSON from response text if wrapped in markdown or other text
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group())
                else:
                    raise ValueError("No valid JSON found in response")

            # Validate that we have a proper dictionary
            if not isinstance(analysis, dict):
                raise ValueError("Response is not a valid JSON object")

            return analysis

        except Exception as e:
            self.logger.error(f"Failed to parse Gemini response: {str(e)}")
            self.logger.debug(f"Raw response: {response_text[:500]}...")
            raise RuntimeError(f"Failed to parse analysis response: {str(e)}")

    
    # Maintain compatibility with original interface
    async def analyze_screenshot(self, image_path: str, html_content: str = "") -> Dict:
        """Main analysis method"""
        return await self.analyze_screenshot_dcgen(image_path, html_content)

    
# Maintain compatibility - alias the new class
class AnalyzerAgent(DCGenAnalyzer):
    """Compatibility alias for existing code"""
    
    def __init__(self, config: SystemConfig, name: str = "AnalyzerAgent"):
        super().__init__(config, name=name)