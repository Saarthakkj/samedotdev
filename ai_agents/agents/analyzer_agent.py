from config.system_config import SystemConfig
from pathlib import Path
import logging
import google.generativeai as genai
import re
import json
from typing import Dict, Optional
import os
import base64
import asyncio
import aiohttp
from bs4 import BeautifulSoup

from google.adk.agents import Agent as ADKAgent  # type: ignore
from google.adk.artifacts import InMemoryArtifactService
from google.genai.types import Part

class AnalyzerAgent(ADKAgent):
    # Declare it as a Pydantic field
    _config: SystemConfig = None

    def __init__(self, config: SystemConfig):
              # 1️⃣ run the ADK / Pydantic constructor first
        super().__init__(
            name="analyzer_agent",
            model="gemini-2.0-flash-exp",
            description="Analyzes screenshots + HTML",
            instruction="Generate cloning specification from screenshot",
            tools=[],
        )
                
        object.__setattr__(self , "_config" , config)
        object.__setattr__(self , "logger" , self._setup_logger()) 
        object.__setattr__(self  , "artifact_service" , InMemoryArtifactService)
        
        
        genai.configure(api_key = self._config.gemini_api_key)
        object.__setattr__(self , "model", self._initialize_gemini_model())
        if self.model is None : 
            raise RuntimeError("failed to inisialize a gemini model")
        
    def _setup_logger(self):
        """Setup logger similar to ScreenshotAgent"""
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(self.__class__.__name__)

    def _initialize_gemini_model(self):
        """Initialize Gemini model with fallback options"""
        model_options = [
            'gemini-2.0-flash-exp',
            'gemini-2.0-flash'
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

    async def analyze_screenshot(self, image_path: str) -> Dict:
        """Main analysis method - async version"""
        self.logger.info(f"Starting analysis for image: {image_path}")
        
        # Validate image file
        if not os.path.exists(image_path):
            self.logger.error(f"Image file not found: {image_path}")
            raise FileNotFoundError(f"Image file not found: {image_path}")

        image_size = os.path.getsize(image_path)
        self.logger.info(f"Image file size: {image_size} bytes")

        # Parse HTML content which may be JSON-encoded with analysis config
        html_text = ""
        analysis_config = {}
        # Perform Gemini analysis
        analysis = await self._gemini_analysis(image_path, html_text)

        # Save analysis as artifact
        try:
            analysis_json = json.dumps(analysis, ensure_ascii=False, indent=2)
            
            # Create Part object with correct method signature
            try:
                # Try creating Part with data and mime_type
                artifact_part = Part(
                    data=analysis_json.encode('utf-8'),
                    mime_type="application/json"
                )
            except Exception as part_error:
                self.logger.debug(f"Failed to create Part with data/mime_type: {part_error}")
                try:
                    # Try the text parameter approach
                    artifact_part = Part(text=analysis_json)
                except Exception as text_error:
                    self.logger.debug(f"Failed to create Part with text: {text_error}")
                    # Skip artifact saving if Part creation fails
                    raise Exception("Could not create Part object")
            
            revision_id = await self.artifact_service.save_artifact(
                app_name="analyzer_app",
                user_id="user_analyzer",
                session_id="session_analyzer",
                filename=f"analysis_{Path(image_path).stem}.json",
                artifact=artifact_part
            )
            self.logger.info(f"Analysis artifact saved with revision ID: {revision_id}")
        
        except Exception as artifact_error:
            self.logger.warning(f"Failed to save artifact: {artifact_error}")
            # Continue without saving artifact - analysis still works

        return analysis

    def analyze_screenshot_sync(self, image_path: str, html_content: str = "") -> Dict:
        """Synchronous version of analysis"""
        return asyncio.run(self.analyze_screenshot(image_path, html_content))

    async def _gemini_analysis(self, image_path: str, html_content: str) -> Dict:
        """Perform analysis using Gemini API"""
        # Read image data
        with open(image_path, 'rb') as img_file:
            image_data = img_file.read()
        self.logger.info(f"Successfully read image data: {len(image_data)} bytes")

        # Create analysis prompt
        prompt = self._create_analysis_prompt(html_content)

        # Perform vision analysis
        self.logger.info("Performing vision analysis with Gemini")
        image_part = {"mime_type": "image/png", "data": image_data}
        response = await self.model.generate_content_async([prompt, image_part])

        if not response or not response.text:
            raise RuntimeError("Empty response from Gemini vision analysis")

        self.logger.info(f"Got response from Gemini: {len(response.text)} characters")
        analysis = self._parse_gemini_response(response.text)
        self._log_analysis_result(analysis, "vision")
        return analysis

    def _create_analysis_prompt(self, html_content: str) -> str:
        """Create comprehensive analysis prompt for Next.js 14"""
        return f"""
        Analyze the provided website screenshot and HTML content to generate a detailed specification for cloning the website using Next.js 14 with the App Router. Extract ALL VISIBLE TEXT from the screenshot using OCR-like capabilities and map it to Next.js components (e.g., layout.jsx, page.jsx, Header.jsx). Combine this with design elements (layout, colors, typography) from both the screenshot and HTML to produce a comprehensive cloning specification.

        HTML CONTENT (first 3000 chars):
        {html_content[:3000] if html_content else "No HTML content provided"}

        INSTRUCTIONS:
        1. Extract all text visible in the screenshot, including headings, paragraphs, buttons, navigation items, and footer text.
        2. Map extracted text to Next.js components (e.g., 'app/layout.jsx', 'app/page.jsx', 'components/Header.jsx').
        3. Identify design elements: layout (grid/flexbox), colors (hex codes), typography (font-family, sizes, weights), and components (header, navigation, etc.).
        4. Provide detailed descriptions in `components_description`, `pages_description`, and `styles_description`, including exact text content for each component.
        5. Ensure `content_structure.text_content` includes a dictionary mapping components to their text content.
        6. Assume Next.js 14 with App Router and React Server Components (add "use client" for interactive components like navigation).
        7. Return a valid JSON object with the structure below, ensuring all fields are populated with accurate data.

        OUTPUT FORMAT:
        {{
            "layout": {{
                "type": "grid|flexbox|float|modern",
                "structure": "header-main-footer|sidebar-main|full-width|dashboard",
                "breakpoints": ["sm:640px", "md:768px", "lg:1024px", "xl:1280px"],
                "component_hierarchy": ["Layout", "Page", "Header", "Navigation", "Main", "Footer"]
            }},
            "colors": {{
                "primary": "#hexcode",
                "secondary": "#hexcode",
                "accent": "#hexcode",
                "background": "#hexcode",
                "text": "#hexcode"
            }},
            "typography": {{
                "primary_font": "font-family-name",
                "font_sizes": ["12px", "14px", "16px", "18px", "24px"],
                "font_weights": [300, 400, 500, 600, 700],
                "line_heights": ["1.2", "1.4", "1.6"]
            }},
            "components": ["app/layout.jsx", "app/page.jsx", "components/Header.jsx", "components/Navigation.jsx", "components/Footer.jsx"],
            "interactive_elements": {{
                "navigation": ["dropdown", "hamburger", "tabs"],
                "buttons": ["primary", "secondary", "outline"],
                "forms": ["text-input", "select", "checkbox"],
                "animations": ["fade", "slide", "scale"]
            }},
            "content_structure": {{
                "sections": ["header", "main", "footer"],
                "text_hierarchy": ["h1", "h2", "h3", "p"],
                "text_content": {{"components/Header.jsx": "Extracted text", "app/page.jsx": "Extracted text", "components/Footer.jsx": "Extracted text"}},
                "images": ["hero-bg", "thumbnails", "icons"],
                "icons": ["fontawesome", "heroicons", "custom"]
            }},
            "cloning_requirements": {{
                "npm_packages": ["next", "react", "react-dom"],
                "component_files": ["components/Header.jsx", "components/Navigation.jsx", "app/page.jsx"],
                "components_description": {{
                    "components/Header.jsx": "Header component with text 'Welcome to Our Site', blue background",
                    "app/page.jsx": "Main page component with text 'About Us', centered content"
                }},
                "pages": ["app/page.jsx", "app/layout.jsx"],
                "pages_description": {{
                    "app/page.jsx": "Main page with header and main content",
                    "app/layout.jsx": "Root layout with navigation and footer"
                }},
                "styles": ["app/globals.css"],
                "styles_description": {{
                    "app/globals.css": "Global styles for layout, typography, and colors"
                }},
                "config_files": {{"next.config.js": {{}}, "package.json": {{}}}},
                "assets": ["public/images/", "public/icons/"],
                "performance_tips": ["lazy-loading", "code-splitting"],
                "package_json": {{
                    "name": "cloned-website",
                    "version": "1.0.0",
                    "scripts": {{"dev": "next dev", "build": "next build", "start": "next start"}},
                    "dependencies": {{"next": "14", "react": "^18", "react-dom": "^18"}},
                    "devDependencies": {{}}
                }}
            }}
        }}

        CONSTRAINTS:
        - Return ONLY valid JSON without markdown or extra text.
        - Ensure text_content includes all extracted text, mapped to Next.js components.
        - Use reasonable defaults for missing information.
        - Include exact hex codes for colors and precise typography details.
        - Assume Next.js 14 conventions (App Router, 'use client' for interactive components).
        """

    def _parse_gemini_response(self, response_text: str) -> Dict:
        """Parse Gemini response into structured analysis"""
        try:
            # Try to parse as JSON first
            try:
                analysis = json.loads(response_text)
            except json.JSONDecodeError:
                # Extract JSON from response text if wrapped in markdown or other text
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group())
                else:
                    raise ValueError("No valid JSON found in response")

            # Validate that we have a proper dictionary
            if not isinstance(analysis, dict):
                raise ValueError("Response is not a valid JSON object")

            # Validate and enhance the analysis
            analysis = self._validate_and_enhance_analysis(analysis)
            
            self._log_analysis_result(analysis, "vision")
            return analysis

        except Exception as e:
            self.logger.error(f"Failed to parse Gemini response: {str(e)}")
            raise RuntimeError(f"Failed to parse analysis response: {str(e)}")

    def _validate_and_enhance_analysis(self, analysis: Dict) -> Dict:
        """Validate and enhance analysis results"""
        required_fields = ["layout", "colors", "typography", "components", "interactive_elements", "content_structure", "cloning_requirements"]
        
        for field in required_fields:
            if field not in analysis:
                self.logger.warning(f"Missing required field: {field}")
                if field == "components":
                    analysis[field] = ["app/layout.jsx", "app/page.jsx", "components/Header.jsx"]
                else:
                    analysis[field] = {}

        # Ensure cloning requirements have required structure
        cloning_req = analysis.get("cloning_requirements", {})
        if not cloning_req.get("package_json"):
            cloning_req["package_json"] = {
                "name": "cloned-website",
                "version": "1.0.0",
                "scripts": {"dev": "next dev", "build": "next build", "start": "next start"},
                "dependencies": {"next": "14", "react": "^18", "react-dom": "^18"},
                "devDependencies": {}
            }

        # Ensure content structure has text content
        content_structure = analysis.get("content_structure", {})
        if not content_structure.get("text_content"):
            self.logger.warning("No text content found in analysis")
            content_structure["text_content"] = {
                "components/Header.jsx": "Header content extracted from screenshot",
                "app/page.jsx": "Main page content extracted from screenshot",
                "components/Footer.jsx": "Footer content extracted from screenshot"
            }

        return analysis

    def _log_analysis_result(self, analysis: Dict, method: str):
        """Log analysis results for debugging"""
        self.logger.info(f"Analysis completed using {method} method")
        self.logger.info(f"Found {len(analysis.get('components', []))} components")
        
        text_content = analysis.get('content_structure', {}).get('text_content', {})
        self.logger.info(f"Extracted text for {len(text_content)} components")
        
        for component, text in text_content.items():
            self.logger.debug(f"{component}: {text[:50]}...")
        
        colors = analysis.get('colors', {})
        self.logger.info(f"Detected colors: {list(colors.keys())}")
        
        layout_type = analysis.get('layout', {}).get('type', 'unknown')
        self.logger.info(f"Layout type: {layout_type}")