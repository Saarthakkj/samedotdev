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
from bs4 import BeautifulSoup  # For HTML text extraction in fallback
# import os
# from dotenv import load_dotenv

# load_dotenv(os.path.join(os.path.dirname(__file__), "../../../.env"))




# Optional: Uncomment for Tesseract OCR fallback
try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

class AnalyzerAgent:
    def __init__(self, config: SystemConfig):
        self.config = config
        self.logger = self._setup_logger()
        
        # Initialize Gemini API
        if hasattr(config, 'gemini_api_key') and config.gemini_api_key:
            self.logger.info("Using Gemini API key for analysis")
            genai.configure(api_key=config.gemini_api_key)
            self.model = self._initialize_gemini_model()
        else:
            self.model = None
            self.logger.warning("No Gemini API key provided, using fallback analysis")

    def _setup_logger(self):
        """Setup logger similar to ScreenshotAgent"""
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

    def _detect_framework_from_html(self, html_content: str) -> Dict:
        """Detect frameworks from HTML content"""
        frameworks = {
            "react": ["react", "_react", "jsx", "data-reactroot", "__REACT_DEVTOOLS"],
            "vue": ["vue", "_vue", "v-", "@click", "data-v-"],
            "angular": ["ng-", "[ng", "angular", "_angular"],
            "next": ["_next", "__next", "next.js"],
            "nuxt": ["_nuxt", "__nuxt", "nuxt.js"],
            "svelte": ["svelte", "_svelte"],
            "bootstrap": ["bootstrap", "btn-", "col-", "container-fluid"],
            "tailwind": ["tailwind", "tw-", "text-", "bg-", "flex", "grid"],
            "material-ui": ["mui", "material-ui", "makeStyles"],
            "chakra": ["chakra-ui", "css-"],
            "wordpress": ["wp-content", "wordpress", "wp-"],
            "shopify": ["shopify", "liquid", "theme_id"]
        }

        detected = {"frameworks": [], "css_frameworks": [], "cms": []}
        html_lower = html_content.lower()

        for framework, indicators in frameworks.items():
            for indicator in indicators:
                if indicator in html_lower:
                    if framework in ["react", "vue", "angular", "next", "nuxt", "svelte"]:
                        detected["frameworks"].append(framework)
                    elif framework in ["bootstrap", "tailwind", "material-ui", "chakra"]:
                        detected["css_frameworks"].append(framework)
                    elif framework in ["wordpress", "shopify"]:
                        detected["cms"].append(framework)
                    break

        return detected

    async def analyze_screenshot(self, image_path: str, html_content: str = "") -> Dict:
        """Main analysis method - async version"""
        self.logger.info(f"Starting analysis for image: {image_path}")
        
        try:
            # Validate image file
            if not os.path.exists(image_path):
                self.logger.error(f"Image file not found: {image_path}")
                raise FileNotFoundError(f"Image file not found: {image_path}")

            image_size = os.path.getsize(image_path)
            self.logger.info(f"Image file size: {image_size} bytes")

            # Parse HTML content which may be JSON-encoded with analysis config
            html_text = ""
            analysis_config = {}
            try:
                if html_content:
                    html_data = json.loads(html_content)
                    html_text = html_data.get('content', '')
                    analysis_config = html_data.get('analysis_config', {})
            except json.JSONDecodeError:
                html_text = html_content

            # Detect frameworks from HTML
            framework_hints = self._detect_framework_from_html(html_text) if html_text else {}
            self.logger.info(f"Framework detection complete: {framework_hints}")

            # Use Gemini for analysis if available
            if self.model:
                return await self._gemini_analysis(image_path, html_text, framework_hints)
            else:
                return self._fallback_analysis(image_path, html_text, framework_hints)

        except Exception as e:
            self.logger.error(f"Analysis failed: {str(e)}")
            return self._fallback_analysis(image_path, html_content, {})

    def analyze_screenshot_sync(self, image_path: str, html_content: str = "") -> Dict:
        """Synchronous version of analysis"""
        try:
            return asyncio.run(self.analyze_screenshot(image_path, html_content))
        except Exception as e:
            self.logger.error(f"Sync analysis failed: {str(e)}")
            framework_hints = self._detect_framework_from_html(html_content) if html_content else {}
            return self._fallback_analysis(image_path, html_content, framework_hints)

    async def _gemini_analysis(self, image_path: str, html_content: str, framework_hints: Dict) -> Dict:
        """Perform analysis using Gemini API"""
        try:
            # Read image data
            with open(image_path, 'rb') as img_file:
                image_data = img_file.read()
            self.logger.info(f"Successfully read image data: {len(image_data)} bytes")

            # Create analysis prompt
            prompt = self._create_analysis_prompt(html_content, framework_hints)

            try:
                # Try vision analysis first
                self.logger.info("Attempting vision analysis with Gemini")
                image_part = {"mime_type": "image/png", "data": image_data}
                response = await self.model.generate_content_async([prompt, image_part])

                if response and response.text:
                    self.logger.info(f"Got response from Gemini: {len(response.text)} characters")
                    analysis = self._parse_gemini_response(response.text, framework_hints)
                    self._log_analysis_result(analysis, "vision")
                    return analysis
                else:
                    self.logger.error("Empty response from Gemini")
                    return self._fallback_analysis(image_path, html_content, framework_hints)

            except Exception as vision_error:
                self.logger.error(f"Vision analysis failed: {vision_error}")
                
                # Fallback to text-only analysis
                try:
                    self.logger.info("Attempting text-only analysis")
                    text_prompt = self._create_text_only_prompt(html_content, framework_hints)
                    response = await self.model.generate_content_async(text_prompt)

                    if response and response.text:
                        self.logger.info("Got response from text-only analysis")
                        analysis = self._parse_gemini_response(response.text, framework_hints)
                        self._log_analysis_result(analysis, "text-only")
                        return analysis
                    else:
                        self.logger.error("Empty response from text-only analysis")
                        return self._fallback_analysis(image_path, html_content, framework_hints)

                except Exception as text_error:
                    self.logger.error(f"Text-only analysis failed: {text_error}")
                    return self._fallback_analysis(image_path, html_content, framework_hints)

        except Exception as e:
            self.logger.error(f"Gemini analysis failed: {str(e)}")
            return self._fallback_analysis(image_path, html_content, framework_hints)

    def _create_analysis_prompt(self, html_content: str, framework_hints: Dict) -> str:
        """Create comprehensive analysis prompt"""
        return f"""
        Analyze the provided website screenshot and HTML content to generate a detailed specification for cloning the website. Extract ALL VISIBLE TEXT from the screenshot using OCR-like capabilities and map it to specific components (e.g., header, main, footer). Combine this with design elements (layout, colors, typography) from both the screenshot and HTML to produce a comprehensive cloning specification.

        FRAMEWORK DETECTION HINTS:
        - JS Frameworks: {framework_hints.get('frameworks', [])}
        - CSS Frameworks: {framework_hints.get('css_frameworks', [])}
        - CMS: {framework_hints.get('cms', [])}

        HTML CONTENT (first 3000 chars):
        {html_content[:3000] if html_content else "No HTML content provided"}

        INSTRUCTIONS:
        1. Extract all text visible in the screenshot, including headings, paragraphs, buttons, navigation items, and footer text.
        2. Map extracted text to components (e.g., "Header: Welcome to Our Site", "Main: About Us").
        3. Identify design elements: framework, CSS framework, colors (hex codes), typography (font-family, sizes, weights), layout (grid/flexbox), and components (header, navigation, etc.).
        4. Provide detailed descriptions in `components_description`, `pages_description`, and `styles_description`, including exact text content for each component.
        5. Ensure `content_structure.text_content` includes a dictionary mapping components to their text content.
        6. Return a valid JSON object with the structure below, ensuring all fields are populated with accurate data.

        OUTPUT FORMAT:
        {{
            "framework": {{
                "primary": "react|vue|angular|next|nuxt|svelte|vanilla|unknown",
                "css": "tailwind|bootstrap|material-ui|chakra|styled-components|css-modules|vanilla|unknown",
                "build_tools": ["vite", "webpack", "parcel"],
                "backend_indicators": ["api", "graphql", "rest"]
            }},
            "layout": {{
                "type": "grid|flexbox|float|modern",
                "structure": "header-main-footer|sidebar-main|full-width|dashboard",
                "breakpoints": ["sm:640px", "md:768px", "lg:1024px", "xl:1280px"],
                "component_hierarchy": ["Header", "Navigation", "Main", "Footer"]
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
            "components": ["header", "navigation", "hero", "cards", "forms", "footer"],
            "interactive_elements": {{
                "navigation": ["dropdown", "hamburger", "tabs"],
                "buttons": ["primary", "secondary", "outline"],
                "forms": ["text-input", "select", "checkbox"],
                "animations": ["fade", "slide", "scale"]
            }},
            "content_structure": {{
                "sections": ["hero", "features", "testimonials", "cta", "footer"],
                "text_hierarchy": ["h1", "h2", "h3", "p"],
                "text_content": {{"header": "Extracted text", "main": "Extracted text", "footer": "Extracted text"}},
                "images": ["hero-bg", "thumbnails", "icons"],
                "icons": ["fontawesome", "heroicons", "custom"]
            }},
            "cloning_requirements": {{
                "npm_packages": ["react", "react-dom", "next", "tailwindcss"],
                "component_files": ["components/Header.html", "components/Main.html"],
                "components_description": {{
                    "components/Header.html": "Header with text 'Welcome to Our Site', blue background, flexbox layout",
                    "components/Main.html": "Main section with text 'About Us', centered content"
                }},
                "pages": ["index.html"],
                "pages_description": {{
                    "index.html": "Main page with header ('Welcome'), main ('About'), and footer ('Copyright')"
                }},
                "styles": ["style.css"],
                "styles_description": {{
                    "style.css": "Styles for layout, typography, and colors, including text styling"
                }},
                "config_files": {{"package.json": {{}}}},
                "assets": ["images/", "icons/"],
                "performance_tips": ["lazy-loading", "code-splitting"],
                "package_json": {{
                    "name": "cloned-website",
                    "version": "1.0.0",
                    "scripts": {{"start": "live-server"}},
                    "dependencies": {{}},
                    "devDependencies": {{"live-server": "^1.2.2"}}
                }}
            }}
        }}

        CONSTRAINTS:
        - Return ONLY valid JSON without markdown or extra text.
        - Ensure text_content includes all extracted text, mapped to components.
        - Use reasonable defaults for missing information (e.g., "unknown" for framework).
        - Include exact hex codes for colors and precise typography details.
        """

    def _create_text_only_prompt(self, html_content: str, framework_hints: Dict) -> str:
        """Create prompt for text-only analysis"""
        return f"""
        Analyze this HTML content to generate a website cloning specification. Extract all text content from the HTML and map it to components (e.g., header, main, footer). Infer design elements from HTML structure, class names, and inline styles.

        FRAMEWORK HINTS: {framework_hints}
        HTML CONTENT: {html_content[:5000] if html_content else "No HTML content provided"}

        Return a JSON object with the same structure as the vision analysis, including:
        - `content_structure.text_content` with extracted text mapped to components.
        - Detailed `components_description` and `pages_description` with exact text content.
        Ensure all fields are populated with reasonable defaults if specific information is missing.
        """

    def _parse_gemini_response(self, response_text: str, framework_hints: Dict = None) -> Dict:
        """Parse Gemini response into structured analysis"""
        try:
            # Try to parse as JSON first
            try:
                analysis = json.loads(response_text)
            except json.JSONDecodeError:
                # If not JSON, try to extract structured data
                analysis = self._extract_from_text_response(response_text, framework_hints)

            # Ensure all required fields are present
            if not isinstance(analysis, dict):
                analysis = {}

            # Add framework information if missing
            if 'framework' not in analysis:
                analysis['framework'] = {
                    'primary': framework_hints.get('frameworks', ['vanilla'])[0] if framework_hints and framework_hints.get('frameworks') else 'vanilla',
                    'css': framework_hints.get('css_frameworks', ['vanilla'])[0] if framework_hints and framework_hints.get('css_frameworks') else 'vanilla'
                }

            # Add components if missing
            if 'components' not in analysis:
                analysis['components'] = []

            # Add styles if missing
            if 'styles' not in analysis:
                analysis['styles'] = {
                    'colors': {},
                    'typography': {},
                    'layout': {}
                }

            # Add structure if missing
            if 'structure' not in analysis:
                analysis['structure'] = {
                    'layout': 'single-page',
                    'sections': ['main']
                }

            # Validate and enhance the analysis
            analysis = self._validate_and_enhance_analysis(analysis, framework_hints)
            
            self.logger.info(f"Analysis complete (vision): Framework={analysis['framework']['primary']}, CSS={analysis['framework']['css']}, Components={len(analysis['components'])}, TextSections={analysis['structure']['sections']}")
            
            return analysis

        except Exception as e:
            self.logger.error(f"Failed to parse Gemini response: {str(e)}")
            return self._create_default_analysis(
                framework=framework_hints.get('frameworks', ['vanilla'])[0] if framework_hints and framework_hints.get('frameworks') else 'vanilla',
                css_framework=framework_hints.get('css_frameworks', ['vanilla'])[0] if framework_hints and framework_hints.get('css_frameworks') else 'vanilla'
            )

    def _validate_and_enhance_analysis(self, analysis: Dict, framework_hints: Dict = None) -> Dict:
        """Validate and enhance analysis results"""
        required_fields = ["framework", "layout", "colors", "typography", "components", "interactive_elements", "content_structure", "cloning_requirements"]
        
        for field in required_fields:
            if field not in analysis:
                analysis[field] = {} if field != "components" else []

        # Apply framework hints
        if framework_hints:
            framework = analysis.get("framework", {})
            if not framework.get("primary") or framework["primary"] == "unknown":
                framework["primary"] = framework_hints.get("frameworks", ["vanilla"])[0] if framework_hints.get("frameworks") else "vanilla"
            if not framework.get("css") or framework["css"] == "unknown":
                framework["css"] = framework_hints.get("css_frameworks", ["vanilla"])[0] if framework_hints.get("css_frameworks") else "vanilla"

        # Ensure cloning requirements
        cloning_req = analysis.get("cloning_requirements", {})
        if not cloning_req.get("package_json"):
            cloning_req["package_json"] = {
                "name": "cloned-website",
                "version": "1.0.0",
                "description": "Cloned website",
                "scripts": {"start": "live-server", "build": "echo 'No build step required'"},
                "dependencies": {},
                "devDependencies": {"live-server": "^1.2.2"}
            }

        # Ensure content structure
        content_structure = analysis.get("content_structure", {})
        if not content_structure.get("text_content"):
            content_structure["text_content"] = {
                "header": "Default header text",
                "main": "Default main content",
                "footer": "Default footer text"
            }

        return analysis

    def _extract_from_text_response(self, response_text: str, framework_hints: Dict = None) -> Dict:
        """Extract analysis from text response when JSON parsing fails"""
        self.logger.info("Attempting text extraction from response")

        detected_framework = framework_hints.get("frameworks", ["vanilla"])[0] if framework_hints and framework_hints.get("frameworks") else "vanilla"
        detected_css = framework_hints.get("css_frameworks", ["vanilla"])[0] if framework_hints and framework_hints.get("css_frameworks") else "vanilla"

        # Extract text content from response
        text_content = {"header": "Welcome to Our Site", "main": "About Us Content", "footer": "Copyright 2025"}
        
        try:
            lines = response_text.split('\n')
            meaningful_lines = [line.strip() for line in lines if line.strip() and len(line.strip()) > 5]
            
            if meaningful_lines:
                # Distribute text across components
                third = len(meaningful_lines) // 3
                if third > 0:
                    text_content["header"] = meaningful_lines[0][:100]
                    text_content["main"] = meaningful_lines[third][:100] if third < len(meaningful_lines) else meaningful_lines[-1][:100]
                    text_content["footer"] = meaningful_lines[-1][:100]
        except Exception as e:
            self.logger.debug(f"Failed to extract text from response: {e}")

        return self._create_default_analysis(detected_framework, detected_css, text_content)

    def _fallback_analysis(self, image_path: str, html_content: str, framework_hints: Dict = None) -> Dict:
        """Fallback analysis method when Gemini is not available"""
        self.logger.info("Using fallback analysis method")

        detected_framework = framework_hints.get("frameworks", ["vanilla"])[0] if framework_hints and framework_hints.get("frameworks") else "vanilla"
        detected_css = framework_hints.get("css_frameworks", ["vanilla"])[0] if framework_hints and framework_hints.get("css_frameworks") else "vanilla"

        # Extract text from HTML using BeautifulSoup
        text_content = self._extract_text_from_html(html_content)
        
        # Try OCR if available and image exists
        if TESSERACT_AVAILABLE and os.path.exists(image_path):
            try:
                ocr_text = self._extract_text_from_image(image_path)
                if ocr_text:
                    # Merge OCR text with HTML text
                    for key in text_content:
                        if not text_content[key] or text_content[key] in ["Default header text", "Main Content", "Copyright 2025"]:
                            if key in ocr_text:
                                text_content[key] = ocr_text[key]
            except Exception as e:
                self.logger.debug(f"OCR extraction failed: {e}")

        # Extract additional info from HTML
        colors = self._extract_colors_from_html(html_content) if html_content else self._get_default_colors()
        typography = self._extract_typography_from_html(html_content) if html_content else self._get_default_typography()
        components = self._detect_components_from_html(html_content) if html_content else ["header", "main", "footer"]

        result = self._create_default_analysis(detected_framework, detected_css, text_content, colors, typography, components)
        result["fallback"] = True
        result["framework_hints_applied"] = framework_hints or {}
        
        self._log_analysis_result(result, "fallback")
        return result

    def _extract_text_from_html(self, html_content: str) -> Dict:
        """Extract text from HTML content"""
        text_content = {
            "header": "Default header text",
            "main": "Main Content",
            "footer": "Copyright 2025"
        }

        if not html_content:
            return text_content

        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract header text
            header = soup.find('header') or soup.find(attrs={"class": re.compile('header', re.I)})
            if header:
                header_text = header.get_text(strip=True)
                if header_text:
                    text_content["header"] = header_text[:100]

            # Extract main content
            main = soup.find('main') or soup.find(attrs={"class": re.compile('main|content', re.I)})
            if main:
                main_text = main.get_text(strip=True)
                if main_text:
                    text_content["main"] = main_text[:100]

            # Extract footer text
            footer = soup.find('footer') or soup.find(attrs={"class": re.compile('footer', re.I)})
            if footer:
                footer_text = footer.get_text(strip=True)
                if footer_text:
                    text_content["footer"] = footer_text[:100]

        except Exception as e:
            self.logger.debug(f"Failed to extract text from HTML: {e}")

        return text_content

    def _extract_text_from_image(self, image_path: str) -> Optional[Dict]:
        """Extract text from image using OCR"""
        if not TESSERACT_AVAILABLE:
            return None

        try:
            img = Image.open(image_path)
            ocr_text = pytesseract.image_to_string(img)
            
            if not ocr_text.strip():
                return None

            lines = [line.strip() for line in ocr_text.split('\n') if line.strip()]
            
            text_content = {}
            if lines:
                # Simple heuristic to distribute text
                num_lines = len(lines)
                if num_lines >= 3:
                    text_content["header"] = lines[0][:100]
                    text_content["main"] = ' '.join(lines[1:-1])[:100]
                    text_content["footer"] = lines[-1][:100]
                elif num_lines == 2:
                    text_content["header"] = lines[0][:100]
                    text_content["main"] = lines[1][:100]
                elif num_lines == 1:
                    text_content["main"] = lines[0][:100]

            return text_content

        except Exception as e:
            self.logger.debug(f"OCR extraction failed: {e}")
            return None

    def _extract_colors_from_html(self, html_content: str) -> Dict:
        """Extract colors from HTML content"""
        colors = self._get_default_colors()

        if not html_content:
            return colors

        color_patterns = [
            r'color:\s*([#\w]+)',
            r'background-color:\s*([#\w]+)',
            r'border-color:\s*([#\w]+)',
            r'#([0-9a-fA-F]{3,6})',
            r'rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)',
            r'rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*[\d.]+\s*\)'
        ]

        found_colors = []
        for pattern in color_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            found_colors.extend(matches)

        # Filter and format colors
        valid_colors = []
        for color in found_colors:
            if isinstance(color, tuple):  # RGB values
                continue
            if color.startswith('#') or (color.isalnum() and len(color) in [3, 6]):
                valid_colors.append(color if color.startswith('#') else f"#{color}")

        # Apply found colors
        if valid_colors:
            unique_colors = list(set(valid_colors))
            if len(unique_colors) >= 1:
                colors["primary"] = unique_colors[0]
            if len(unique_colors) >= 2:
                colors["secondary"] = unique_colors[1]
            if len(unique_colors) >= 3:
                colors["accent"] = unique_colors[2]

        return colors

    def _extract_typography_from_html(self, html_content: str) -> Dict:
        """Extract typography information from HTML"""
        typography = self._get_default_typography()

        if not html_content:
            return typography

        # Font family extraction
        font_family_matches = re.findall(r'font-family:\s*([^;]+)', html_content, re.IGNORECASE)
        if font_family_matches:
            typography["primary_font"] = font_family_matches[0].strip().replace('"', '').replace("'", "")

        # Font size extraction
        font_size_matches = re.findall(r'font-size:\s*(\d+(?:px|em|rem|%))', html_content, re.IGNORECASE)
        if font_size_matches:
            typography["font_sizes"] = list(set(font_size_matches))[:5]

        # Font weight extraction
        font_weight_matches = re.findall(r'font-weight:\s*(\d+)', html_content, re.IGNORECASE)
        if font_weight_matches:
            weights = [int(w) for w in font_weight_matches if w.isdigit()]
            if weights:
                typography["font_weights"] = sorted(list(set(weights)))

        # Line height extraction
        line_height_matches = re.findall(r'line-height:\s*([\d.]+)', html_content, re.IGNORECASE)
        if line_height_matches:
            typography["line_heights"] = list(set(line_height_matches))[:3]

        return typography

    def _detect_components_from_html(self, html_content: str) -> list:
        """Detect components from HTML content"""
        if not html_content:
            return ["header", "main", "footer"]

        components = []
        component_indicators = {
            "header": ["<header", "class.*header", "id.*header"],
            "navigation": ["<nav", "class.*nav", "navbar", "menu"],
            "hero": ["class.*hero", "class.*banner", "class.*jumbotron"],
            "main": ["<main", "class.*main", "id.*main"],
            "content": ["class.*content", "class.*article"],
            "sidebar": ["class.*sidebar", "class.*aside", "<aside"],
            "footer": ["<footer", "class.*footer", "id.*footer"],
            "card": ["class.*card", "class.*tile"],
            "form": ["<form", "class.*form"],
            "button": ["<button", "class.*btn"],
            "modal": ["class.*modal", "class.*popup"],
            "carousel": ["class.*carousel", "class.*slider"],
            "gallery": ["class.*gallery", "class.*grid"]
        }

        html_lower = html_content.lower()
        for component, patterns in component_indicators.items():
            for pattern in patterns:
                if re.search(pattern, html_lower):
                    if component not in components:
                        components.append(component)
                    break

        # Ensure basic components
        basic_components = ["header", "main", "footer"]
        for basic in basic_components:
            if basic not in components:
                components.append(basic)

        return components

    def _get_default_colors(self) -> Dict:
        """Get default color scheme"""
        return {
            "primary": "#3b82f6",
            "secondary": "#f8fafc",
            "accent": "#10b981",
            "background": "#ffffff",
            "text": "#111827"
        }

    def _get_default_typography(self) -> Dict:
        """Get default typography settings"""
        return {
            "primary_font": "system-ui",
            "font_sizes": ["14px", "16px", "18px", "24px", "32px"],
            "font_weights": [400, 500, 600, 700],
            "line_heights": ["1.4", "1.6", "1.8"]
        }

    def _get_packages_for_framework(self, framework: str, css_framework: str) -> list:
        """Get required packages for framework"""
        base_packages = []
        
        if framework == "react":
            base_packages = ["react", "react-dom"]
        elif framework == "next":
            base_packages = ["next", "react", "react-dom"]
        elif framework == "vue":
            base_packages = ["vue"]
        elif framework == "angular":
            base_packages = ["@angular/core", "@angular/common"]
        elif framework == "vanilla":
            base_packages = ["live-server"]

        if css_framework == "tailwind":
            base_packages.extend(["tailwindcss", "autoprefixer", "postcss"])
        elif css_framework == "bootstrap":
            base_packages.extend(["bootstrap"])
        elif css_framework == "material-ui":
            base_packages.extend(["@mui/material", "@emotion/react", "@emotion/styled"])
        elif css_framework == "chakra":
            base_packages.extend(["@chakra-ui/react", "@emotion/react", "@emotion/styled"])

        return base_packages

    def _create_default_analysis(self, framework: str = "vanilla", css_framework: str = "vanilla", 
                                text_content: Dict = None, colors: Dict = None, 
                                typography: Dict = None, components: list = None) -> Dict:
        """Create default analysis structure"""
        if text_content is None:
            text_content = {
                "header": "Welcome to Our Site",
                "main": "Main Content Area",
                "footer": "Copyright 2025"
            }
        
        if colors is None:
            colors = self._get_default_colors()
        
        if typography is None:
            typography = self._get_default_typography()
        
        if components is None:
            components = ["header", "main", "footer"]

        packages = self._get_packages_for_framework(framework, css_framework)

        return {
            "framework": {
                "primary": framework,
                "css": css_framework,
                "build_tools": ["vite"] if framework in ["react", "vue"] else ["live-server"],
                "backend_indicators": []
            },
            "layout": {
                "type": "flexbox",
                "structure": "header-main-footer",
                "breakpoints": ["sm:640px", "md:768px", "lg:1024px", "xl:1280px"],
                "component_hierarchy": ["Header", "Main", "Footer"]
            },
            "colors": colors,
            "typography": typography,
            "components": components,
            "interactive_elements": {
                "navigation": ["basic"],
                "buttons": ["primary", "secondary"],
                "forms": ["text-input"],
                "animations": ["fade"]
            },
            "content_structure": {
                "sections": ["header", "main", "footer"],
                "text_hierarchy": ["h1", "h2", "p"],
                "text_content": text_content,
                "images": [],
                "icons": ["basic"]
            },
            "cloning_requirements": {
                "npm_packages": packages,
                "component_files": [
                    f"components/Header.{self._get_file_extension(framework)}",
                    f"components/Main.{self._get_file_extension(framework)}",
                    f"components/Footer.{self._get_file_extension(framework)}"
                ],
                "components_description": {
                    f"components/Header.{self._get_file_extension(framework)}": f"Header component with text: '{text_content.get('header', 'Header text')}'",
                    f"components/Main.{self._get_file_extension(framework)}": f"Main content component with text: '{text_content.get('main', 'Main content')}'",
                    f"components/Footer.{self._get_file_extension(framework)}": f"Footer component with text: '{text_content.get('footer', 'Footer text')}'"
                },
                "pages": [f"index.{self._get_file_extension(framework)}"],
                "pages_description": {
                    f"index.{self._get_file_extension(framework)}": f"Main page with header ('{text_content.get('header', 'Header')}'), main content ('{text_content.get('main', 'Main')}'), and footer ('{text_content.get('footer', 'Footer')}')"
                },
                "styles": ["styles.css"] if css_framework == "vanilla" else [f"{css_framework}.config.js"],
                "styles_description": {
                    "styles.css" if css_framework == "vanilla" else f"{css_framework}.config.js": f"Styling configuration for {css_framework} framework with colors: {colors.get('primary', '#3b82f6')} (primary), {colors.get('secondary', '#f8fafc')} (secondary)"
                },
                "config_files": self._get_config_files(framework, css_framework),
                "assets": ["images/", "icons/"],
                "performance_tips": ["optimize-images", "minify-css", "lazy-loading"],
                "package_json": {
                    "name": "cloned-website",
                    "version": "1.0.0",
                    "description": "Cloned website generated by AnalyzerAgent",
                    "main": f"index.{self._get_file_extension(framework)}",
                    "scripts": self._get_scripts(framework),
                    "dependencies": {pkg: "latest" for pkg in packages if not pkg.startswith("@types/")},
                    "devDependencies": self._get_dev_dependencies(framework, css_framework)
                }
            }
        }

    def _get_file_extension(self, framework: str) -> str:
        """Get appropriate file extension for framework"""
        extensions = {
            "react": "jsx",
            "next": "jsx",
            "vue": "vue",
            "angular": "ts",
            "svelte": "svelte",
            "vanilla": "html"
        }
        return extensions.get(framework, "html")

    def _get_config_files(self, framework: str, css_framework: str) -> Dict:
        """Get configuration files for framework"""
        config_files = {"package.json": {}}
        
        if framework in ["react", "next", "vue"]:
            config_files["vite.config.js"] = {}
        
        if css_framework == "tailwind":
            config_files["tailwind.config.js"] = {}
            config_files["postcss.config.js"] = {}
        
        if framework == "next":
            config_files["next.config.js"] = {}
        
        if framework == "angular":
            config_files["angular.json"] = {}
            config_files["tsconfig.json"] = {}
        
        return config_files

    def _get_scripts(self, framework: str) -> Dict:
        """Get npm scripts for framework"""
        scripts = {
            "react": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview"
            },
            "next": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start"
            },
            "vue": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview"
            },
            "angular": {
                "dev": "ng serve",
                "build": "ng build",
                "test": "ng test"
            },
            "vanilla": {
                "start": "live-server",
                "build": "echo 'No build step required'"
            }
        }
        return scripts.get(framework, scripts["vanilla"])

    def _get_dev_dependencies(self, framework: str, css_framework: str) -> Dict:
        """Get development dependencies for framework"""
        dev_deps = {}
        
        if framework in ["react", "next", "vue"]:
            dev_deps.update({
                "vite": "latest",
                "@vitejs/plugin-react": "latest" if framework in ["react", "next"] else "latest"
            })
        
        if framework == "vanilla":
            dev_deps["live-server"] = "^1.2.2"
        
        if css_framework == "tailwind":
            dev_deps.update({
                "tailwindcss": "latest",
                "autoprefixer": "latest",
                "postcss": "latest"
            })
        
        if framework == "angular":
            dev_deps.update({
                "@angular/cli": "latest",
                "@angular-devkit/build-angular": "latest",
                "typescript": "latest"
            })
        
        return dev_deps

    def _log_analysis_result(self, analysis: Dict, method: str):
        """Log analysis results for debugging"""
        try:
            framework = analysis.get("framework", {}).get("primary", "unknown")
            css_framework = analysis.get("framework", {}).get("css", "unknown")
            components_count = len(analysis.get("components", []))
            text_content_keys = list(analysis.get("content_structure", {}).get("text_content", {}).keys())
            
            self.logger.info(f"Analysis complete ({method}): "
                           f"Framework={framework}, CSS={css_framework}, "
                           f"Components={components_count}, TextSections={text_content_keys}")
            
            # Log package.json info
            package_json = analysis.get("cloning_requirements", {}).get("package_json", {})
            dependencies_count = len(package_json.get("dependencies", {}))
            dev_dependencies_count = len(package_json.get("devDependencies", {}))
            
            self.logger.info(f"Package info: {dependencies_count} dependencies, "
                           f"{dev_dependencies_count} dev dependencies")
            
        except Exception as e:
            self.logger.debug(f"Failed to log analysis result: {e}")

    async def batch_analyze(self, image_paths: list, html_contents: list = None) -> list:
        """Analyze multiple screenshots in batch"""
        self.logger.info(f"Starting batch analysis for {len(image_paths)} images")
        
        if html_contents is None:
            html_contents = [""] * len(image_paths)
        
        results = []
        for i, (image_path, html_content) in enumerate(zip(image_paths, html_contents)):
            try:
                self.logger.info(f"Processing image {i+1}/{len(image_paths)}: {image_path}")
                result = await self.analyze_screenshot(image_path, html_content)
                result["batch_index"] = i
                result["source_image"] = image_path
                results.append(result)
                
                # Add small delay to avoid rate limiting
                await asyncio.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Failed to analyze image {i+1}: {e}")
                # Add error result
                error_result = self._create_default_analysis()
                error_result["error"] = str(e)
                error_result["batch_index"] = i
                error_result["source_image"] = image_path
                results.append(error_result)
        
        self.logger.info(f"Batch analysis complete: {len(results)} results")
        return results

    def save_analysis(self, analysis: Dict, output_path: str):
        """Save analysis results to file"""
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Analysis saved to: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to save analysis: {e}")
            raise

    def load_analysis(self, input_path: str) -> Dict:
        """Load analysis results from file"""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                analysis = json.load(f)
            
            self.logger.info(f"Analysis loaded from: {input_path}")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Failed to load analysis: {e}")
            raise

    def get_analysis_summary(self, analysis: Dict) -> Dict:
        """Get a summary of the analysis results"""
        try:
            framework = analysis.get("framework", {})
            content_structure = analysis.get("content_structure", {})
            cloning_requirements = analysis.get("cloning_requirements", {})
            
            summary = {
                "framework_info": {
                    "primary": framework.get("primary", "unknown"),
                    "css": framework.get("css", "unknown"),
                    "build_tools": framework.get("build_tools", [])
                },
                "content_summary": {
                    "sections": len(content_structure.get("sections", [])),
                    "text_sections": len(content_structure.get("text_content", {})),
                    "components": len(analysis.get("components", []))
                },
                "technical_requirements": {
                    "npm_packages": len(cloning_requirements.get("npm_packages", [])),
                    "component_files": len(cloning_requirements.get("component_files", [])),
                    "pages": len(cloning_requirements.get("pages", [])),
                    "config_files": len(cloning_requirements.get("config_files", {}))
                },
                "complexity_score": self._calculate_complexity_score(analysis),
                "estimated_development_time": self._estimate_development_time(analysis)
            }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Failed to generate analysis summary: {e}")
            return {"error": str(e)}

    def _calculate_complexity_score(self, analysis: Dict) -> int:
        """Calculate complexity score (1-10) based on analysis"""
        score = 1
        
        # Framework complexity
        framework = analysis.get("framework", {}).get("primary", "vanilla")
        framework_scores = {
            "vanilla": 1, "react": 3, "vue": 3, "next": 4, 
            "angular": 5, "svelte": 2
        }
        score += framework_scores.get(framework, 1)
        
        # Component complexity
        components = analysis.get("components", [])
        score += min(len(components) // 3, 3)  # Max 3 points for components
        
        # Interactive elements
        interactive = analysis.get("interactive_elements", {})
        interactive_count = sum(len(v) if isinstance(v, list) else 1 for v in interactive.values())
        score += min(interactive_count // 2, 2)  # Max 2 points for interactivity
        
        # CSS framework complexity
        css_framework = analysis.get("framework", {}).get("css", "vanilla")
        if css_framework != "vanilla":
            score += 1
        
        return min(score, 10)

    def _estimate_development_time(self, analysis: Dict) -> str:
        """Estimate development time based on complexity"""
        complexity = self._calculate_complexity_score(analysis)
        
        time_estimates = {
            1: "1-2 hours",
            2: "2-4 hours", 
            3: "4-8 hours",
            4: "8-12 hours",
            5: "1-2 days",
            6: "2-3 days",
            7: "3-5 days",
            8: "5-7 days",
            9: "1-2 weeks",
            10: "2+ weeks"
        }
        
        return time_estimates.get(complexity, "Unknown")

    def __del__(self):
        """Cleanup method"""
        try:
            if hasattr(self, 'logger'):
                self.logger.info("AnalyzerAgent cleanup complete")
        except:
            pass  # Ignore cleanup errors
