import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional
import asyncio
import google.generativeai as genai
from config.system_config import SystemConfig

class GeneratorAgent:
    def __init__(self, config: SystemConfig):
        self.config = config
        self.logger = self._setup_logger()
        
        # Initialize Gemini API
        if hasattr(config, 'gemini_api_key') and config.gemini_api_key:
            self.logger.info("Using Gemini API key for generation")
            genai.configure(api_key=config.gemini_api_key)
            self.model = self._initialize_gemini_model()
        else:
            self.model = None
            self.logger.error("No Gemini API key provided, cannot generate code")
            raise ValueError("Gemini API key is required for GeneratorAgent")

    def _setup_logger(self):
        """Setup logger for GeneratorAgent"""
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(self.__class__.__name__)

    def _initialize_gemini_model(self):
        """Initialize Gemini model"""
        model_options = [
            'gemini-2.0-flash-exp',
            'gemini-2.0-flash',
            'gemini-1.5-pro',
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
        raise ValueError("No suitable Gemini model available")

    async def generate_code(self, analysis: Dict, output_dir: str) -> Dict:
        """
        Generate code based on analysis - this is the method your orchestrator is calling
        This is an alias for generate_website to maintain compatibility
        """
        return await self.generate_website(analysis, output_dir)

    async def generate_website(self, analysis: Dict, output_dir: str) -> Dict:
        """Generate website based on analysis using Gemini"""
        self.logger.info(f"Starting website generation for output directory: {output_dir}")
        
        try:
            # Validate analysis
            if not analysis or not isinstance(analysis, dict):
                self.logger.error("Invalid analysis provided")
                raise ValueError("Invalid analysis structure")

            # Create output directory
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            # Generate project structure and code
            generated_files = await self._generate_project_files(analysis, output_path)
            
            # Save generated files
            for file_path, content in generated_files.items():
                full_path = output_path / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.logger.info(f"Generated file: {full_path}")

            # Return generation result
            result = {
                "status": "success",
                "generated_files": list(generated_files.keys()),
                "output_directory": str(output_path.absolute()),
                "framework": analysis.get("framework", {}).get("primary", "unknown"),
                "css_framework": analysis.get("framework", {}).get("css", "unknown")
            }
            self.logger.info(f"Website generation completed successfully")
            return result

        except Exception as e:
            self.logger.error(f"Website generation failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "generated_files": [],
                "output_directory": output_dir
            }

    async def _generate_project_files(self, analysis: Dict, output_path: Path) -> Dict[str, str]:
        """Generate all project files based on analysis"""
        generated_files = {}
        
        # Create prompt based on analysis
        prompt = self._create_generation_prompt(analysis)
        
        try:
            # Generate code using Gemini
            response = await self.model.generate_content_async(prompt)
            
            if not response or not response.text:
                raise ValueError("Empty response from Gemini")

            # Parse response to extract files
            files = self._parse_gemini_response(response.text)
            
            # Process each file
            for file_path, content in files.items():
                # Clean file path
                clean_path = self._clean_file_path(file_path)
                generated_files[clean_path] = content
                
                # Ensure package.json includes necessary dependencies
                if clean_path == "package.json":
                    generated_files[clean_path] = self._enhance_package_json(
                        content,
                        analysis.get("cloning_requirements", {}).get("package_json", {})
                    )

            # Add any missing critical files
            generated_files = self._ensure_critical_files(generated_files, analysis)
            
            return generated_files

        except Exception as e:
            self.logger.error(f"Failed to generate project files: {str(e)}")
            raise

    def _create_generation_prompt(self, analysis: Dict) -> str:
        """Create prompt for code generation"""
        framework = analysis.get("framework", {}).get("primary", "vanilla")
        css_framework = analysis.get("framework", {}).get("css", "vanilla")
        colors = analysis.get("colors", {})
        typography = analysis.get("typography", {})
        components = analysis.get("components", [])
        content_structure = analysis.get("content_structure", {})
        cloning_requirements = analysis.get("cloning_requirements", {})

        return f"""
        You are an expert web developer tasked with generating a complete, production-ready website based on the following analysis. Do not use templates; generate all code from scratch using the specifications provided. Create a fully-featured, beautiful website that matches the analysis exactly.

        SYSTEM CONSTRAINTS:
        - Use WebContainer environment (browser-based Node.js runtime)
        - Prefer Vite for web server
        - Use only pure JavaScript/JSX, no native binaries
        - Use only standard Python library if Python is needed
        - Prefer SQLite or libsql for databases
        - Use 2-space indentation
        - Split functionality into small, reusable modules
        - Use valid URLs for images (Unsplash stock photos)
        - Use lucide-react for icons

        WEBSITE SPECIFICATIONS:
        Framework:
        - Primary: {framework}
        - CSS: {css_framework}
        - Build Tools: {json.dumps(analysis.get('framework', {}).get('build_tools', []))}
        
        Colors:
        - Primary: {colors.get('primary', '#3b82f6')}
        - Secondary: {colors.get('secondary', '#f8fafc')}
        - Accent: {colors.get('accent', '#10b981')}
        - Background: {colors.get('background', '#ffffff')}
        - Text: {colors.get('text', '#111827')}

        Typography:
        - Primary Font: {typography.get('primary_font', 'system-ui')}
        - Font Sizes: {json.dumps(typography.get('font_sizes', ['14px', '16px', '18px']))}
        - Font Weights: {json.dumps(typography.get('font_weights', [400, 500, 600]))}
        - Line Heights: {json.dumps(typography.get('line_heights', ['1.4', '1.6']))}

        Components: {json.dumps(components)}
        
        Content Structure:
        - Sections: {json.dumps(content_structure.get('sections', []))}
        - Text Content: {json.dumps(content_structure.get('text_content', {}))}
        - Images: {json.dumps(content_structure.get('images', []))}
        - Icons: {json.dumps(content_structure.get('icons', []))}

        Interactive Elements:
        - Navigation: {json.dumps(analysis.get('interactive_elements', {}).get('navigation', []))}
        - Buttons: {json.dumps(analysis.get('interactive_elements', {}).get('buttons', []))}
        - Forms: {json.dumps(analysis.get('interactive_elements', {}).get('forms', []))}
        - Animations: {json.dumps(analysis.get('interactive_elements', {}).get('animations', []))}

        Cloning Requirements:
        - NPM Packages: {json.dumps(cloning_requirements.get('npm_packages', []))}
        - Component Files: {json.dumps(cloning_requirements.get('component_files', []))}
        - Pages: {json.dumps(cloning_requirements.get('pages', []))}
        - Styles: {json.dumps(cloning_requirements.get('styles', []))}
        - Config Files: {json.dumps(list(cloning_requirements.get('config_files', {}).keys()))}

        INSTRUCTIONS:
        1. Generate a complete website matching the analysis specifications
        2. Use {framework} with {css_framework} for styling
        3. Create all necessary files (index.html/jsx, components, styles, configs)
        4. Include package.json with all required dependencies
        5. Use Vite as the development server
        6. Implement all components, interactive elements, and animations
        7. Use exact text content from text_content
        8. Apply specified colors and typography
        9. Create modular, maintainable code
        10. Return output as a JSON object with file paths as keys and content as values
        11. Include setup commands in package.json scripts
        12. Use Unsplash URLs for images and lucide-react for icons

        OUTPUT FORMAT:
        Return ONLY a valid JSON object with no additional text or formatting:
        {{
            "package.json": "...",
            "index.html": "...",
            "src/App.jsx": "...",
            "src/main.jsx": "...",
            "src/styles.css": "...",
            "vite.config.js": "..."
        }}
        """
        
    def _parse_gemini_response(self, response_text: str) -> Dict[str, str]:
        """Parse Gemini response into file structure"""
        try:
            # Clean response text - remove any markdown formatting
            clean_text = response_text.strip()
            
            # Try to find JSON within the response
            if clean_text.startswith('```json'):
                # Extract JSON from markdown code block
                start = clean_text.find('{')
                end = clean_text.rfind('}') + 1
                if start != -1 and end > start:
                    clean_text = clean_text[start:end]
            elif clean_text.startswith('```'):
                # Extract from generic code block
                lines = clean_text.split('\n')
                json_lines = []
                in_json = False
                for line in lines:
                    if line.strip().startswith('```') and not in_json:
                        in_json = True
                        continue
                    elif line.strip().startswith('```') and in_json:
                        break
                    elif in_json:
                        json_lines.append(line)
                clean_text = '\n'.join(json_lines)
            
            # Try to parse as JSON
            files = json.loads(clean_text)
            if not isinstance(files, dict):
                raise ValueError("Response is not a valid file structure JSON")
            return files
            
        except json.JSONDecodeError as e:
            self.logger.warning(f"Failed to parse response as JSON: {e}")
            self.logger.debug(f"Response text: {response_text[:500]}...")
            
            # Fallback: Try to create basic files
            return self._create_fallback_files()

    def _create_fallback_files(self) -> Dict[str, str]:
        """Create basic fallback files when parsing fails"""
        return {
            "package.json": json.dumps({
                "name": "generated-website",
                "version": "1.0.0",
                "private": True,
                "type": "module",
                "scripts": {
                    "dev": "vite",
                    "build": "vite build",
                    "preview": "vite preview"
                },
                "dependencies": {
                    "react": "^18.2.0",
                    "react-dom": "^18.2.0",
                    "lucide-react": "^0.263.1"
                },
                "devDependencies": {
                    "vite": "^4.4.5",
                    "@vitejs/plugin-react": "^4.0.3"
                }
            }, indent=2),
            "index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Website</title>
</head>
<body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
</body>
</html>""",
            "src/main.jsx": """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './styles.css'

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
)""",
            "src/App.jsx": """import React from 'react'

function App() {
    return (
        <div className="app">
            <h1>Generated Website</h1>
            <p>This is a fallback generated website.</p>
        </div>
    )
}

export default App""",
            "src/styles.css": """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: system-ui, -apple-system, sans-serif;
    line-height: 1.6;
    color: #333;
}

.app {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}""",
            "vite.config.js": """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [react()]
})"""
        }

    def _clean_file_path(self, file_path: str) -> str:
        """Clean and normalize file path"""
        # Remove any leading slashes or invalid characters
        clean_path = file_path.strip().lstrip('/').replace('..', '').replace('~', '')
        
        # Ensure proper extension
        if not Path(clean_path).suffix:
            if 'html' in clean_path.lower():
                clean_path += '.html'
            elif 'css' in clean_path.lower():
                clean_path += '.css'
            elif 'js' in clean_path.lower() or 'jsx' in clean_path.lower():
                clean_path += '.jsx'
                
        return clean_path

    def _enhance_package_json(self, generated_content: str, analysis_package_json: Dict) -> str:
        """Enhance package.json with necessary dependencies"""
        try:
            package_data = json.loads(generated_content)
        except json.JSONDecodeError:
            self.logger.warning("Invalid package.json content, creating new one")
            package_data = {
                "name": "generated-website",
                "version": "1.0.0",
                "private": True,
                "scripts": {},
                "dependencies": {},
                "devDependencies": {}
            }

        # Merge scripts
        package_data["scripts"] = {
            **package_data.get("scripts", {}),
            **analysis_package_json.get("scripts", {}),
            "dev": "vite",
            "build": "vite build",
            "preview": "vite preview"
        }

        # Merge dependencies
        package_data["dependencies"] = {
            **package_data.get("dependencies", {}),
            **analysis_package_json.get("dependencies", {}),
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "lucide-react": "^0.263.1"
        }

        # Merge devDependencies
        package_data["devDependencies"] = {
            **package_data.get("devDependencies", {}),
            **analysis_package_json.get("devDependencies", {}),
            "vite": "^4.4.5",
            "@vitejs/plugin-react": "^4.0.3"
        }

        # Add type module for JSX
        package_data["type"] = "module"

        return json.dumps(package_data, indent=2)

    def _ensure_critical_files(self, generated_files: Dict[str, str], analysis: Dict) -> Dict[str, str]:
        """Ensure all critical files are present"""
        framework = analysis.get("framework", {}).get("primary", "vanilla")
        
        # Ensure package.json
        if "package.json" not in generated_files:
            generated_files["package.json"] = json.dumps({
                "name": "generated-website",
                "version": "1.0.0",
                "private": True,
                "type": "module",
                "scripts": {
                    "dev": "vite",
                    "build": "vite build",
                    "preview": "vite preview"
                },
                "dependencies": {
                    "react": "^18.2.0",
                    "react-dom": "^18.2.0",
                    "lucide-react": "^0.263.1"
                },
                "devDependencies": {
                    "vite": "^4.4.5",
                    "@vitejs/plugin-react": "^4.0.3"
                }
            }, indent=2)

        # Ensure index.html
        if "index.html" not in generated_files:
            generated_files["index.html"] = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Website</title>
</head>
<body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
</body>
</html>
"""

        # Ensure main.jsx
        if "src/main.jsx" not in generated_files:
            generated_files["src/main.jsx"] = """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './styles.css'

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
)
"""

        # Ensure App.jsx
        if "src/App.jsx" not in generated_files:
            generated_files["src/App.jsx"] = """import React from 'react'

function App() {
    return (
        <div className="app">
            <h1>Generated Website</h1>
            <p>Welcome to your generated website!</p>
        </div>
    )
}

export default App
"""

        # Ensure styles.css
        if "src/styles.css" not in generated_files:
            generated_files["src/styles.css"] = """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: system-ui, -apple-system, sans-serif;
    line-height: 1.6;
    color: #333;
}

.app {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}
"""

        # Ensure vite.config.js
        if "vite.config.js" not in generated_files:
            generated_files["vite.config.js"] = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [react()]
})
"""

        return generated_files

    async def batch_generate(self, analyses: List[Dict], output_base_dir: str) -> List[Dict]:
        """Generate multiple websites in batch"""
        self.logger.info(f"Starting batch generation for {len(analyses)} analyses")
        
        results = []
        for i, analysis in enumerate(analyses):
            try:
                output_dir = os.path.join(output_base_dir, f"website_{i}")
                result = await self.generate_website(analysis, output_dir)
                result["batch_index"] = i
                results.append(result)
                
                # Add small delay to avoid rate limiting
                await asyncio.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Failed to generate website {i+1}: {str(e)}")
                results.append({
                    "status": "error",
                    "error": str(e),
                    "generated_files": [],
                    "output_directory": os.path.join(output_base_dir, f"website_{i}"),
                    "batch_index": i
                })
        
        self.logger.info(f"Batch generation complete: {len(results)} results")
        return results

    def save_generation_result(self, result: Dict, output_path: str):
        """Save generation result to file"""
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Generation result saved to: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to save generation result: {e}")
            raise

    def __del__(self):
        """Cleanup method"""
        try:
            if hasattr(self, 'logger'):
                self.logger.info("GeneratorAgent cleanup complete")
        except:
            pass