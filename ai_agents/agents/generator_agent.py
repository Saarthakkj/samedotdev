import asyncio
import time
from typing import Dict, List
import logging
from pathlib import Path
import json
import re
from tqdm.auto import tqdm
import google.generativeai as genai

class RateLimitedDCGenGenerator:
    """Enhanced DCGen generator with AI-driven prompts and rate limiting"""
    
    # Valid Lucide React icons list (commonly used ones)
    VALID_LUCIDE_ICONS = [
        'Home', 'User', 'Settings', 'Search', 'Menu', 'X', 'ChevronDown', 'ChevronUp', 
        'ChevronLeft', 'ChevronRight', 'Plus', 'Minus', 'Edit', 'Trash2', 'Save', 
        'Download', 'Upload', 'Mail', 'Phone', 'MapPin', 'Calendar', 'Clock', 'Star',
        'Heart', 'ThumbsUp', 'Share', 'Eye', 'EyeOff', 'Lock', 'Unlock', 'Check',
        'AlertCircle', 'Info', 'HelpCircle', 'Filter', 'Sort', 'Grid', 'List',
        'Image', 'Play', 'Pause', 'Volume2', 'VolumeX', 'Wifi', 'Battery', 'Signal',
        'ShoppingCart', 'CreditCard', 'Truck', 'Package', 'Gift', 'Tag', 'Percent',
        'DollarSign', 'TrendingUp', 'TrendingDown', 'BarChart', 'PieChart', 'Activity',
        'Users', 'UserPlus', 'MessageCircle', 'Send', 'Bell', 'BellOff', 'Bookmark',
        'Flag', 'Globe', 'Zap', 'Coffee', 'Sun', 'Moon', 'Cloud', 'Umbrella',
        'Car', 'Plane', 'Train', 'Bike', 'Camera', 'Video', 'Music', 'Headphones',
        'Monitor', 'Smartphone', 'Tablet', 'Laptop', 'Mouse', 'Keyboard', 'Printer',
        'Folder', 'File', 'FileText', 'Database', 'Server', 'Code', 'Terminal',
        'Book', 'BookOpen', 'Newspaper', 'PenTool', 'Scissors', 'Palette', 'Brush'
    ]
    
    def __init__(self, config):
        self.config = config
        self.logger = self._setup_logger()
        
        # Rate limiting configuration
        self.requests_per_minute = 8
        self.request_interval = 60 / self.requests_per_minute
        self.last_request_time = 0
        self.max_retries = 3
        self.base_retry_delay = 10
        
        if not hasattr(config, 'gemini_api_key') or not config.gemini_api_key:
            raise ValueError("Gemini API key is required")
        
        genai.configure(api_key=config.gemini_api_key)
        self.model = self._initialize_gemini_model()
        
        if not self.model:
            raise ValueError("No suitable Gemini model available")

    def _setup_logger(self):
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(self.__class__.__name__)

    def _initialize_gemini_model(self):
        model_options = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-2.0-flash']
        for model_name in model_options:
            try:
                model = genai.GenerativeModel(model_name)
                self.logger.info(f"Initialized {model_name}")
                return model
            except Exception as e:
                self.logger.warning(f"Failed to initialize {model_name}: {e}")
                continue
        raise ValueError("Failed to initialize any Gemini model")

    async def _rate_limited_request(self, prompt: str, retry_count: int = 0) -> str:
        """Make rate-limited API request with exponential backoff"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.request_interval:
            wait_time = self.request_interval - time_since_last_request
            self.logger.info(f"Rate limiting: waiting {wait_time:.1f} seconds")
            await asyncio.sleep(wait_time)
        
        try:
            self.last_request_time = time.time()
            response = await self.model.generate_content_async(prompt)
            
            if not response or not response.text:
                raise Exception("Empty response from API")
            
            return response.text
            
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"API request failed (attempt {retry_count + 1}): {error_msg}")
            
            if "quota" in error_msg.lower() or "rate" in error_msg.lower() or "429" in error_msg:
                if retry_count < self.max_retries:
                    retry_delay = self._extract_retry_delay(error_msg)
                    if retry_delay is None:
                        retry_delay = self.base_retry_delay * (2 ** retry_count)
                    
                    self.logger.info(f"Rate limit hit. Retrying in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                    return await self._rate_limited_request(prompt, retry_count + 1)
                else:
                    raise Exception(f"Rate limit exceeded after {self.max_retries} retries")
            
            if retry_count < self.max_retries:
                retry_delay = self.base_retry_delay * (2 ** retry_count)
                self.logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                return await self._rate_limited_request(prompt, retry_count + 1)
            
            raise e

    def _extract_retry_delay(self, error_message: str) -> int:
        """Extract retry delay from error message"""
        retry_match = re.search(r'retry_delay.*?seconds:\s*(\d+)', error_message)
        if retry_match:
            return int(retry_match.group(1))
        return None

    def _get_base_prompt(self) -> str:
        """Get the base prompt with all requirements"""
        valid_icons_str = ', '.join(self.VALID_LUCIDE_ICONS)
        
        return f"""
        CRITICAL REQUIREMENTS:
        1. Generate VALID JSX code only - no TypeScript syntax, no interface definitions
        2. Use only these VALID Lucide React icons: {valid_icons_str}
        3. Import lucide-react icons ONLY when actually used: import {{ IconName }} from 'lucide-react'
        4. For Next.js 14 app directory imports:
           - Components: import ComponentName from '../components/ComponentName'
           - Use relative paths correctly
        5. All code must be production-ready and beautiful, not cookie-cutter
        6. Use Tailwind CSS classes for styling
        7. Use valid Unsplash URLs: https://images.unsplash.com/photo-[photo-id]?w=[width]&h=[height]&fit=crop
        8. No markdown formatting in responses - return pure code only
        9. Ensure proper JSX syntax with proper closing tags and React patterns
        10. Add any additional npm packages needed to package.json dependencies
        
        EXAMPLE VALID JSX COMPONENT:
        ```jsx
        import {{ Home, User, Settings }} from 'lucide-react';
        
        export default function ExampleComponent() {{
          return (
            <div className="flex items-center space-x-4">
              <Home className="w-6 h-6" />
              <span>Valid JSX Component</span>
            </div>
          );
        }}
        ```
        """

    async def generate_dcgen_website(self, analysis: Dict, output_dir: str) -> Dict:
        """Generate complete Next.js project structure with AI-driven prompts"""
        self.logger.info(f"Starting AI-driven DCGen generation for: {output_dir}")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate project structure with AI
        self.logger.info("Generating project structure with AI...")
        project_structure = await self._generate_project_structure_with_ai(analysis)
        
        # Generate all files with AI
        generated_files = await self._generate_all_files_with_ai(analysis, project_structure)
        
        # Write files to disk
        await self._write_files(generated_files, output_path)
        
        return {
            "status": "success",
            "output_directory": str(output_path),
            "generated_files": list(generated_files.keys()),
            "total_files": len(generated_files)
        }

    async def _generate_project_structure_with_ai(self, analysis: Dict) -> Dict:
        """Generate project structure using AI prompts"""
        base_prompt = self._get_base_prompt()

        structure_prompt = f"""
        {base_prompt}
        
        Based on the following analysis, create a complete Next.js 14 project structure with all essential files:
        
        ANALYSIS DATA:
        {json.dumps(analysis, indent=2)}
        
        Generate a JSON response with the following structure:
        {{
            "essential_files": {{
                "package.json": {{"type": "config", "description": "Next.js project dependencies"}},
                "postcss.config.js": {{"type": "config", "description": "PostCSS configuration"}},
                "tailwind.config.js": {{"type": "config", "description": "Tailwind CSS configuration"}},
                "next.config.js": {{"type": "config", "description": "Next.js configuration"}},
                "app/layout.jsx": {{"type": "layout", "description": "Root layout component"}},
                "app/page.jsx": {{"type": "page", "description": "Main page component"}},
                "app/globals.css": {{"type": "styles", "description": "Global CSS with Tailwind"}},
                "components/[ComponentName].jsx": {{"type": "component", "description": "Component based on analysis"}}
            }},
            "components_to_generate": [
                // List of components based on the analysis
            ],
             "file_generation_order": [
                "package.json",
                "postcss.config.js",
                "tailwind.config.js",
                "next.config.js",
                "app/globals.css",
                "app/layout.jsx",
                "app/page.jsx",
                "components/[ComponentName].jsx"
                // Other components
                // List of files in the desired generation order
            ]
        }}
        
        IMPORTANT: Analyze the provided data and determine what components are needed. Create a pixel-perfect clone structure based on the analysis.
        Return ONLY the JSON object, no explanations, no markdown, no extra text.
        """
        
        response_text = await self._rate_limited_request(structure_prompt)
        
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            else:
                raise Exception("No valid JSON structure found in AI response")
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse project structure: {e}")
    
    async def _generate_all_files_with_ai(self, analysis: Dict, project_structure: Dict) -> Dict[str, str]:
        """Generate all files using AI prompts"""
        essential_files = project_structure.get('essential_files', {})
        components_to_generate = project_structure.get('components_to_generate', [])
        file_order = project_structure.get('file_generation_order', list(essential_files.keys()))
        
        generated_files = {}
        
        with tqdm(total=len(file_order), desc="Generating files with AI") as pbar:
            for file_path in file_order:
                try:
                    pbar.set_description(f"AI generating {file_path}")
                    
                    content = await self._generate_file_with_ai(file_path, analysis, essential_files, components_to_generate)
                    generated_files[file_path] = content
                    
                    pbar.update(1)
                    self.logger.info(f"AI generated: {file_path}")
                    
                except Exception as e:
                    self.logger.error(f"Failed to generate {file_path}: {e}")
                    #
                    pbar.update(1)
        
        return generated_files

    async def _generate_file_with_ai(self, file_path: str, analysis: Dict, essential_files: Dict, components_to_generate: List) -> str:
        """Generate individual file using AI"""
        base_prompt = self._get_base_prompt()
        
        if file_path == 'package.json':
            prompt = f"""
            {base_prompt}
            
            Create a package.json file for Next.js 14 with app router that includes:
            - Next.js 14+ with React 18+
            - Tailwind CSS and PostCSS
            - Lucide React for icons
            - Any additional packages that might be needed based on analysis
            - Proper scripts (dev, build, start, lint)
            
            ANALYSIS DATA:
            {json.dumps(analysis, indent=2)}
            
            Return ONLY the JSON content:
            """
            
        elif file_path == 'postcss.config.js':
            prompt = """
            {base_prompt}
             /** @type {import('postcss').Config} */
            module.exports = {
            plugins: {
                tailwindcss: {},
                autoprefixer: {},
            },
            }
            
            Create a postcss.config.js file for Next.js 14 with Tailwind CSS.
            Return ONLY the JavaScript content:
            """
            
        elif file_path == 'tailwind.config.js':
            prompt = f"""
            {base_prompt}
            
            Create a tailwind.config.js for Next.js 14 app directory with:
            - Correct content paths: ['./pages/**/*.{{js,ts,jsx,tsx,mdx}}', './components/**/*.{{js,ts,jsx,tsx,mdx}}', './app/**/*.{{js,ts,jsx,tsx,mdx}}']
            - Custom theme based on analysis if needed
            
            ANALYSIS DATA:
            {json.dumps(analysis.get('visual_analysis', {}), indent=2)}
            
            Return ONLY the JavaScript content:
            """
            
        elif file_path == 'next.config.js':
            prompt = f"""
            {base_prompt}
            
            Create a next.config.js for Next.js 14 with:
            - Image optimization for Unsplash
            - Any other optimizations needed
            
            Return ONLY the JavaScript content:
            """
            
        elif file_path == 'app/layout.jsx':
            prompt = f"""
            {base_prompt}
            
            Create app/layout.jsx for Next.js 14 that:
            - Imports './globals.css'
            - Has proper metadata
            - Uses valid JSX syntax
            - Has clean HTML structure
            
            Return ONLY the JSX content:
            """
            
        elif file_path == 'app/page.jsx':
            prompt = f"""
            {base_prompt}
            
            Create app/page.jsx that:
            - Imports components using: import ComponentName from '../components/ComponentName'
            - Uses components: {', '.join(components_to_generate)}
            - Creates layout based on analysis
            - Uses valid JSX syntax only
            - Only imports lucide-react icons that are actually used
            
            ANALYSIS DATA:
            {json.dumps(analysis, indent=2)}
            
            AVAILABLE COMPONENTS: {components_to_generate}
            
            Return ONLY the JSX content:
            """
            
        elif file_path == 'app/globals.css':
            prompt = f"""
            {base_prompt}
            
            Create app/globals.css with:
            - @tailwind base;
            - @tailwind components;  
            - @tailwind utilities;
            - Any custom styles based on analysis
            
            ANALYSIS DATA:
            {json.dumps(analysis.get('visual_analysis', {}), indent=2)}
            
            Return ONLY the CSS content:
            """
            
        elif file_path.startswith('components/'):
            component_name = file_path.split('/')[-1].replace('.jsx', '')
            prompt = f"""
            {base_prompt}
            
            Create a {component_name} React component that:
            - Uses valid JSX syntax (no TypeScript)
            - Only imports lucide-react icons that are actually used from the valid list
            - Uses Tailwind CSS for styling
            - Is production-ready and beautiful
            - Uses proper Unsplash URLs if images needed
            - Based on the analysis data provided
            
            VALID LUCIDE ICONS: {', '.join(self.VALID_LUCIDE_ICONS)}
            
            ANALYSIS DATA:
            {json.dumps(analysis, indent=2)}
            
            Return ONLY the JSX component code with export default:
            """
            
        else:
            raise Exception(f"Unknown file type: {file_path}")
        
        response = await self._rate_limited_request(prompt)
        return self._extract_and_validate_code(response, file_path)

    def _extract_and_validate_code(self, response_text: str, file_path: str) -> str:
        """Extract and validate code from AI response"""
        # Remove markdown code blocks if present
        code_block_pattern = r'```(?:\w+)?\s*\n?(.*?)\n?```'
        match = re.search(code_block_pattern, response_text, re.DOTALL)
        
        if match:
            code = match.group(1).strip()
        else:
            code = response_text.strip()
        
        # Validate JSX files for common issues
        if file_path.endswith('.jsx'):
            code = self._validate_jsx_code(code, file_path)
        
        return code

    def _validate_jsx_code(self, code: str, file_path: str) -> str:
        """Validate and fix common JSX issues"""
        # Remove TypeScript interface definitions
        code = re.sub(r'interface\s+\w+\s*\{[^}]+\}', '', code, flags=re.MULTILINE)
        
        # Fix invalid lucide imports - only keep valid ones
        import_pattern = r'import\s*\{\s*([^}]+)\s*\}\s*from\s*[\'"]lucide-react[\'"]'
        import_match = re.search(import_pattern, code)
        
        if import_match:
            imported_icons = [icon.strip() for icon in import_match.group(1).split(',')]
            valid_imported = [icon for icon in imported_icons if icon in self.VALID_LUCIDE_ICONS]
            
            if valid_imported:
                new_import = f"import {{ {', '.join(valid_imported)} }} from 'lucide-react';"
                code = re.sub(import_pattern, new_import, code)
            else:
                # Remove lucide import if no valid icons
                code = re.sub(import_pattern + r'\s*', '', code)
        
        # Fix component imports in app/page.jsx
        if file_path == 'app/page.jsx':
            # Fix relative imports
            code = re.sub(r'from\s*[\'"]@/components/', "from '../components/", code)
            code = re.sub(r'from\s*[\'"]~/components/', "from '../components/", code)
        
        return code
    
    async def _write_files(self, files: Dict[str, str], output_path: Path):
        """Write generated files to disk"""
        for file_path, content in files.items():
            full_path = output_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Written: {full_path}")

    async def generate_website(self, analysis: Dict, output_dir: str) -> Dict:
        """Main entry point for website generation"""
        return await self.generate_dcgen_website(analysis, output_dir)

class GeneratorAgent(RateLimitedDCGenGenerator):
    """Main generator agent class"""
    pass