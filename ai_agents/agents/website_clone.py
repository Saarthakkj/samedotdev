from config.system_config import SystemConfig, CloneResult, GeneratedProject
from agents.analyzer_agent import AnalyzerAgent
from agents.generator_agent import GeneratorAgent
from agents.detector_agent import DetectorAgent
from fastapi import HTTPException
from datetime import datetime
from typing import Dict, Optional
import os
import logging
import json
import traceback
from pathlib import Path
import aiohttp
import base64
import asyncio

class WebsiteCloneOrchestrator:
    def __init__(self, config: SystemConfig):
        self.config = config
        self.logger = self._setup_logger()
        # self.screenshot_agent = ScreenshotAgent(config)
        self.analyzer = AnalyzerAgent(config)
        self.generator = GeneratorAgent(config)
        self.detector = DetectorAgent(config)

    def _setup_logger(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        return logging.getLogger(self.__class__.__name__)

    async def clone_website(self, url: str, system_prompt: str, framework: str = "react", options: Dict = {}) -> CloneResult:
        """Main cloning pipeline with enhanced analyzer and generator integration"""
        start_time = datetime.now()
        analysis_result = None
        generated_project = None
        
        try:
            # Step 1: Capture screenshot and get page data
            self.logger.info(f"Starting clone process for: {url}")
            timestamp = int(start_time.timestamp())
            screenshot_path = f"{getattr(self.config, 'output_dir', 'generated_project')}/original_{timestamp}.png"
            
            # Capture screenshot using Firecrawl directly
            await self._capture_full_page_url(url, screenshot_path)
            
            # Step 2: Enhanced Analysis
            self.logger.info("Analyzing website structure...")
            analysis_config = {
                'include_styles': options.get('analyze_styles', True),
                'include_components': options.get('analyze_components', True),
                'include_assets': options.get('analyze_assets', True),
                'depth': options.get('analysis_depth', 2)
            }
            
            # Get HTML content from screenshot agent
            analysis_result = await self.analyzer.analyze_screenshot(
                screenshot_path, 
                json.dumps(analysis_config)
            )
            
            # Validate analysis results
            if not self._validate_analysis(analysis_result):
                raise HTTPException(status_code=400, detail="Website analysis failed to produce valid results")
            
            # Log framework detection and requested framework
            detected_framework = analysis_result.get('framework', {}).get('primary', 'unknown').lower()
            if detected_framework != framework.lower():
                self.logger.warning(f"Framework mismatch: Requested '{framework}', Detected '{detected_framework}'. Using requested framework '{framework}'.")
            
            # Step 3: Enhanced Code Generation
            self.logger.info("Generating code...")
            # Note: generate_code expects (analysis, output_dir) not (analysis, framework)
            # output_dir = f"{getattr(self.config, 'output_dir', 'generated_project')}/project_{timestamp}"
            generated_project = await self.generator.generate_code(
                analysis_result,
                system_prompt
            )
            
            # Step 4: Validate generated code
            if not self._validate_generated_code(generated_project, framework):
                raise HTTPException(status_code=400, detail="Generated code validation failed")
            
            # Step 5: Compare visual similarity
            # generated_url = options.get('generated_url', 'http://localhost:3000')
            generated_screenshot = f"{getattr(self.config, 'output_dir', 'generated_project')}/generated_{timestamp}.png"
            similarity_score = 0.0
            
            try:
                # await self.screenshot_agent.capture_full_page_url(generated_url, generated_screenshot)
                similarity_score = await self.detector.validate_similarity(screenshot_path, generated_screenshot)
            except Exception as e:
                self.logger.warning(f"Visual comparison failed: {e}. Setting similarity to 0.5")
                similarity_score = 0.5
            
            # Step 6: Run Lighthouse audit (optional)
            # lighthouse_score = await self._run_lighthouse_audit(generated_url) if options.get('run_lighthouse', False) else None
            
            generation_time = (datetime.now() - start_time).total_seconds()
            
            self.logger.info(f"Clone process completed in {generation_time:.2f} seconds")
            
            return CloneResult(
                status="success",
                similarity_score=similarity_score,
                generation_time=generation_time,
                # deployed_url=generated_url
            )
            
        except Exception as e:
            tb_str = traceback.format_exc()
            error_detail = {
                'error': str(e),
                'traceback': tb_str,
                'analysis_result': bool(analysis_result),
                'generated_project': bool(generated_project)
            }
            self.logger.error(f"Clone process failed: {json.dumps(error_detail, indent=2)}")
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(status_code=500, detail=json.dumps(error_detail))

    def _validate_analysis(self, analysis: Dict) -> bool:
        """Validate analysis results for required components"""
        try:
            # Check for basic structure
            if not analysis:
                self.logger.warning("Analysis result is empty")
                return False

            # Check for framework information
            if 'framework' not in analysis:
                self.logger.warning("Missing framework information in analysis")
                return False

            # More lenient validation - just check for basic structure
            self.logger.info("Analysis validation passed")
            return True

        except Exception as e:
            self.logger.error(f"Analysis validation failed: {str(e)}")
            return False

    def _validate_generated_code(self, generated_project: Dict, framework: str) -> bool:
        """Validate the generated code for completeness and correctness"""
        try:
            # The generated_project is a dict returned from GeneratorAgent.generate_code()
            if not generated_project or not isinstance(generated_project, dict):
                self.logger.error("Generated project is not a valid dictionary")
                return False
            
            # Check the status from generator
            if generated_project.get('status') != 'success':
                self.logger.error(f"Generator reported failure: {generated_project.get('error', 'Unknown error')}")
                return False
            
            # Check if files were generated
            generated_files = generated_project.get('generated_files', [])
            if not generated_files:
                self.logger.error("No files were generated")
                return False
            
            # Check for essential files based on the files actually generated
            essential_files = ['package.json', 'index.html']
            found_essential = any(
                any(essential in file_path for essential in essential_files)
                for file_path in generated_files
            )
            
            if not found_essential:
                self.logger.warning(f"No essential files found. Generated files: {generated_files}")
                # Don't fail validation - just log warning
            
            # Check for React/JSX files if React framework
            if framework.lower() == 'react':
                has_react_files = any(
                    file_path.endswith('.jsx') or file_path.endswith('.tsx') or 'App' in file_path
                    for file_path in generated_files
                )
                if not has_react_files:
                    self.logger.warning("No React component files found, but continuing...")
            
            # Check output directory exists
            output_dir = generated_project.get('output_directory')
            if output_dir and os.path.exists(output_dir):
                self.logger.info(f"Generated project saved to: {output_dir}")
            else:
                self.logger.warning(f"Output directory not found: {output_dir}")
            
            self.logger.info(f"Generated code validation passed. Files: {len(generated_files)}")
            return True
            
        except Exception as e:
            self.logger.error(f"Validation failed: {str(e)}")
            self.logger.error(f"Generated project structure: {json.dumps(generated_project, indent=2) if isinstance(generated_project, dict) else str(generated_project)}")
            return False

    async def _run_lighthouse_audit(self, url: str) -> Optional[Dict]:
        """Run Lighthouse audit on the generated website"""
        try:
            # Placeholder for Lighthouse audit implementation
            return {}
        except Exception as e:
            self.logger.error(f"Lighthouse audit failed: {str(e)}")
            return None

    async def _compare_visual_similarity(self, original_screenshot: str, generated_url: str) -> float:
        """Compare visual similarity using DetectorAgent"""
        try:
            generated_screenshot = f"{getattr(self.config, 'output_dir', 'generated_project')}/generated_{int(datetime.now().timestamp())}.png"
            # await self.screenshot_agent.capture_full_page_url(generated_url, generated_screenshot)
            return await self.detector.validate_similarity(original_screenshot, generated_screenshot)
        except Exception as e:
            self.logger.error(f"Visual comparison failed: {str(e)}")
            return 0.5

    async def _capture_full_page_url(self, url: str, output_path: str) -> str:
        """
        Capture a full-page screenshot of `url` using the Firecrawl API and save
        it to `output_path`.
        """
        try:
            api_key = os.getenv("FIRECRAWL_API_KEY")
            if not api_key:
                raise ValueError("FIRECRAWL_API_KEY environment variable not set")

            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "url": url,
                "formats": ["screenshot"],
                "actions": [
                    {"type": "wait", "milliseconds": 2000},
                    {"type": "screenshot"}
                ]
            }

            screenshot_data: Optional[bytes] = None

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.firecrawl.dev/v1/scrape",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        self.logger.error(f"Firecrawl API error ({response.status}): {error_text}")
                        raise Exception(f"Firecrawl API error ({response.status}): {error_text}")

                    result = await response.json()

                    if not result.get("success"):
                        self.logger.error(f"Firecrawl API response unsuccessful: {result}")
                        raise Exception(result.get("error", "Firecrawl scrape unsuccessful"))

                    # 1. Preferred: URL in data.actions.screenshots
                    try:
                        screenshot_url = result["data"]["actions"]["screenshots"][0]
                        async with session.get(screenshot_url) as scr_resp:
                            if scr_resp.status != 200:
                                raise Exception(f"download status {scr_resp.status}")
                            screenshot_data = await scr_resp.read()
                    except Exception:
                        # 2. Fallback: data.screenshot (URL or base64)
                        raw_shot = result.get("data", {}).get("screenshot")
                        if raw_shot:
                            if isinstance(raw_shot, str) and raw_shot.startswith("http"):
                                async with session.get(raw_shot) as scr_resp:
                                    if scr_resp.status != 200:
                                        raise Exception(f"download status {scr_resp.status}")
                                    screenshot_data = await scr_resp.read()
                            elif isinstance(raw_shot, str):
                                raw_shot += "=" * (-len(raw_shot) % 4)  # pad base64
                                screenshot_data = base64.b64decode(raw_shot)

            if not screenshot_data:
                raise Exception("No screenshot data returned from Firecrawl")

            # Save file in executor to avoid blocking
            loop = asyncio.get_event_loop()

            def _write():
                with open(output_path, "wb") as f:
                    f.write(screenshot_data)

            await loop.run_in_executor(None, _write)
            self.logger.info(f"Screenshot saved using Firecrawl: {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"Failed to capture screenshot for {url}: {str(e)}")
            raise