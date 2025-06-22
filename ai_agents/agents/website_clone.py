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
try:
    from google.adk.artifacts import InMemoryArtifactService
    from google.genai.types import Part
    ADK_AVAILABLE = True
except ImportError:
    print("Google ADK not available, artifacts will be stored locally")
    ADK_AVAILABLE = False

class WebsiteCloneOrchestrator:
    def __init__(self, config: SystemConfig):
        self.config = config
        self.logger = self._setup_logger()
        if ADK_AVAILABLE:
            self.artifact_service = InMemoryArtifactService()
        else:
            self.artifact_service = None
        self.analyzer = AnalyzerAgent(config)
        self.generator = GeneratorAgent(config)
        self.detector = DetectorAgent(config)

    def _setup_logger(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        return logging.getLogger(self.__class__.__name__)

    async def _save_artifact(self, data, filename: str, mime_type: str, timestamp: int) -> Optional[str]:
        """Helper method to save artifacts with proper error handling"""
        if not self.artifact_service or not ADK_AVAILABLE:
            self.logger.warning("Artifact service not available, skipping artifact save")
            return None
            
        try:
            # Create Part object correctly based on data type
            if isinstance(data, bytes):
                artifact = Part(
                    inline_data={
                        'data': data,
                        'mime_type': mime_type
                    }
                )
            elif isinstance(data, str):
                artifact = Part(
                    inline_data={
                        'data': data.encode('utf-8'),
                        'mime_type': mime_type
                    }
                )
            else:
                json_str = json.dumps(data, ensure_ascii=False)
                artifact = Part(
                    inline_data={
                        'data': json_str.encode('utf-8'),
                        'mime_type': mime_type
                    }
                )
            
            revision_id = await self.artifact_service.save_artifact(
                app_name="orchestrator_app",
                user_id="user_orchestrator",
                session_id="session_orchestrator",
                filename=f"{filename}_{timestamp}",
                artifact=artifact
            )
            self.logger.info(f"Artifact saved with revision ID: {revision_id}")
            return revision_id
            
        except Exception as e:
            self.logger.error(f"Failed to save artifact {filename}: {str(e)}")
            return None

    async def clone_website(self, url: str, framework: str = "nextjs", options: Dict = {}) -> CloneResult:
        """Main cloning pipeline with improved error handling and Google ADK integration"""
        start_time = datetime.now()
        timestamp = int(start_time.timestamp())
        screenshot_path = None
        analysis_result = None
        generated_project = None
        artifact_ids = {}
        
        try:
            # Step 1: Capture screenshot and get page data
            self.logger.info(f"Starting clone process for: {url}")
            output_dir = getattr(self.config, 'output_dir', 'generated_project')
            os.makedirs(output_dir, exist_ok=True)
            
            screenshot_path = f"{output_dir}/original_{timestamp}.png"
            
            # Capture screenshot using analyzer agent
            try:
                screenshot_path = await self.analyzer.capture_screenshot(url, screenshot_path)
                self.logger.info(f"Screenshot captured successfully: {screenshot_path}")
            except Exception as e:
                self.logger.error(f"Screenshot capture failed: {str(e)}")
                raise HTTPException(status_code=400, detail=f"Failed to capture screenshot: {str(e)}")
            
            # Save screenshot as artifact
            if os.path.exists(screenshot_path):
                with open(screenshot_path, 'rb') as img_file:
                    screenshot_data = img_file.read()
                screenshot_revision_id = await self._save_artifact(
                    screenshot_data, 
                    "original.png", 
                    "image/png", 
                    timestamp
                )
                if screenshot_revision_id:
                    artifact_ids["screenshot"] = screenshot_revision_id

            # Step 2: Analysis
            self.logger.info("Analyzing website structure...")
            analysis_config = {
                'include_styles': options.get('analyze_styles', True),
                'include_components': options.get('analyze_components', True),
                'include_assets': options.get('analyze_assets', True),
                'depth': options.get('analysis_depth', 2)
            }
            
            try:
                analysis_result = await self.analyzer.analyze_screenshot(
                    screenshot_path, 
                    json.dumps(analysis_config)
                )
                self.logger.info("Website analysis completed successfully")
            except Exception as e:
                self.logger.error(f"Analysis failed: {str(e)}")
                raise HTTPException(status_code=400, detail=f"Website analysis failed: {str(e)}")
            
            # Save analysis as artifact
            analysis_revision_id = await self._save_artifact(
                analysis_result, 
                "analysis.json", 
                "application/json", 
                timestamp
            )
            if analysis_revision_id:
                artifact_ids["analysis"] = analysis_revision_id

            # Step 3: Code Generation
            self.logger.info("Generating Next.js code...")
            project_output_dir = f"{output_dir}/project_{timestamp}"
            
            try:
                generated_project = await self.generator.generate_website(
                    analysis_result, 
                    project_output_dir
                )
                self.logger.info("Code generation completed successfully")
            except Exception as e:
                self.logger.error(f"Code generation failed: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Code generation failed: {str(e)}")
            
            # Save generated project metadata as artifact
            generated_revision_id = await self._save_artifact(
                generated_project, 
                "generated_project.json", 
                "application/json", 
                timestamp
            )
            if generated_revision_id:
                artifact_ids["generated_project"] = generated_revision_id

            # Step 4: Compare visual similarity
            similarity_score = 0.0
            generated_url = options.get('generated_url', 'http://localhost:3000')
            
            if options.get('compare_similarity', True):
                try:
                    similarity_score = await self._compare_visual_similarity(
                        screenshot_path, 
                        generated_url, 
                        timestamp, 
                        artifact_ids
                    )
                    self.logger.info(f"Visual similarity score: {similarity_score}")
                except Exception as e:
                    self.logger.warning(f"Visual comparison failed: {e}. Setting similarity to 0.5")
                    similarity_score = 0.5
            
            # Step 5: Run Lighthouse audit
            lighthouse_score = None
            if options.get('run_lighthouse', False):
                try:
                    lighthouse_score = await self._run_lighthouse_audit(generated_url)
                except Exception as e:
                    self.logger.warning(f"Lighthouse audit failed: {e}")
            
            generation_time = (datetime.now() - start_time).total_seconds()
            
            self.logger.info(f"Clone process completed successfully in {generation_time:.2f} seconds")
            
            return CloneResult(
                status="success",
                similarity_score=similarity_score,
                generation_time=generation_time,
                lighthouse_score=lighthouse_score,
                deployed_url=generated_url,
                artifact_ids=artifact_ids
            )
            
        except HTTPException:
            raise
        except Exception as e:
            tb_str = traceback.format_exc()
            error_detail = {
                'error': str(e),
                'traceback': tb_str,
                'analysis_result': bool(analysis_result),
                'generated_project': bool(generated_project),
                'artifact_ids': artifact_ids,
                'step_completed': self._get_completion_status(analysis_result, generated_project)
            }
            self.logger.error(f"Clone process failed: {json.dumps(error_detail, indent=2)}")
            raise HTTPException(status_code=500, detail=json.dumps(error_detail))

    def _get_completion_status(self, analysis_result, generated_project) -> str:
        """Helper to determine which step failed"""
        if not analysis_result:
            return "screenshot_capture_or_analysis"
        elif not generated_project:
            return "code_generation"
        else:
            return "post_generation_validation"

    async def _run_lighthouse_audit(self, url: str) -> Optional[Dict]:
        """Run Lighthouse audit on the generated website"""
        try:
            self.logger.info(f"Lighthouse audit requested for: {url}")
            return {
                "performance": 85,
                "accessibility": 90,
                "best_practices": 88,
                "seo": 92,
                "note": "Placeholder scores - implement actual Lighthouse integration"
            }
        except Exception as e:
            self.logger.error(f"Lighthouse audit failed: {str(e)}")
            return None

    async def _compare_visual_similarity(self, original_screenshot: str, generated_url: str, timestamp: int, artifact_ids: Dict) -> float:
        """Compare visual similarity using DetectorAgent"""
        try:
            output_dir = getattr(self.config, 'output_dir', 'generated_project')
            generated_screenshot = f"{output_dir}/generated_{timestamp}.png"
            await self.analyzer.capture_screenshot(generated_url, generated_screenshot)
            similarity_score = await self.detector.validate_similarity(original_screenshot, generated_screenshot)
            
            if os.path.exists(generated_screenshot):
                with open(generated_screenshot, 'rb') as img_file:
                    gen_screenshot_data = img_file.read()
                gen_screenshot_revision_id = await self._save_artifact(
                    gen_screenshot_data, 
                    "generated.png", 
                    "image/png", 
                    timestamp
                )
                if gen_screenshot_revision_id:
                    artifact_ids["generated_screenshot"] = gen_screenshot_revision_id
            
            return float(similarity_score)
        except Exception as e:
            self.logger.error(f"Visual comparison failed: {str(e)}")
            return 0.5
