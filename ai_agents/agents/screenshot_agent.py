from google.adk.agents import LlmAgent
from google.adk.tools import BaseTool, ToolContext
from google.adk.runners import InMemoryRunner
from google.adk.artifacts import InMemoryArtifactService
from google.genai.types import Part
from pathlib import Path
import logging
import requests
import base64
from typing import Dict, Optional, Any
import asyncio
import aiohttp
import os
import json

class ScreenshotTool(BaseTool):
    """Full-page screenshot capture tool using Firecrawl API"""
    
    def __init__(self, artifact_service: InMemoryArtifactService):
        super().__init__(
            name="screenshot_tool",
            description="Capture full-page screenshots of websites using Firecrawl API with optimized settings for complete page capture"
        )
        self.firecrawl_api_key = os.getenv('FIRECRAWL_API_KEY')
        self.firecrawl_base_url = "https://api.firecrawl.dev"
        self.artifact_service = artifact_service
        self.logger = self._setup_logger()
        
        if not self.firecrawl_api_key:
            self.logger.error("Firecrawl API key not found in environment")
            raise ValueError("FIRECRAWL_API_KEY environment variable is required")

    def _setup_logger(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        return logging.getLogger(self.__class__.__name__)

    async def execute(self, context: ToolContext, **kwargs) -> Dict[str, Any]:
        """Main execution method for the full-page screenshot tool"""
        try:
            url = kwargs.get('url')
            output_path = kwargs.get('output_path', 'screenshots/screenshot.png')
            screenshot_options = kwargs.get('options', {})
            
            if not url:
                self.logger.error("URL parameter is required")
                return {
                    "success": False,
                    "error": "URL parameter is required",
                    "result": None
                }
            
            # Create output directory
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Capture full-page screenshot with enhanced options
            result_path = await self._capture_full_page_screenshot(url, output_path, screenshot_options)
            
            # Save as artifact
            try:
                with open(result_path, 'rb') as f:
                    artifact_data = f.read()
                # Use correct Part constructor
                artifact_part = Part(
                    inline_data={
                        'data': artifact_data,
                        'mime_type': 'image/png'
                    }
                )
                revision_id = await self.artifact_service.save_artifact(
                    app_name="screenshot_app",
                    user_id="user_screenshot",
                    session_id="session_screenshot",
                    filename=Path(result_path).name,
                    artifact=artifact_part
                )
                self.logger.info(f"Full-page screenshot artifact saved with revision ID: {revision_id}")
            except Exception as e:
                self.logger.warning(f"Failed to save artifact for {result_path}: {str(e)}")
                # Continue execution even if artifact save fails
            
            return {
                "success": True,
                "result": {
                    "screenshot_path": result_path,
                    "url": url,
                    "screenshot_type": "full-page",
                    "message": f"Full-page screenshot successfully captured and saved to {result_path}"
                },
                "error": None
            }
            
        except Exception as e:
            self.logger.error(f"Full-page screenshot capture failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "result": None
            }

    async def _capture_full_page_screenshot(self, url: str, output_path: str, options: Dict = None) -> str:
        """Capture full-page screenshot using Firecrawl API with optimized settings"""
        if not self.firecrawl_api_key:
            raise ValueError("Firecrawl API key is required")

        headers = {
            "Authorization": f"Bearer {self.firecrawl_api_key}",
            "Content-Type": "application/json"
        }
        
        # Enhanced full-page screenshot options
        default_options = {
            "waitFor": 3000,  # Longer wait for full page load
            "mobile": False,   # Desktop view for full content
            "timeout": 30000   # Extended timeout for large pages
        }
        
        # Merge user options with defaults, prioritizing full-page capture
        merged_options = {**default_options, **(options or {})}
        
        wait_time = merged_options.get("waitFor", 3000)
        timeout = merged_options.get("timeout", 30000)
        
        payload = {
            "url": url,
            "formats": ["screenshot@fullPage"],
            "actions": [
                {"type": "wait", "milliseconds": wait_time},
                {"type": "screenshot"}
            ],
            "timeout": timeout
        }

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout/1000)) as session:
            try:
                self.logger.info(f"Capturing full-page screenshot for: {url}")
                async with session.post(
                    f"{self.firecrawl_base_url}/v1/scrape",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        self.logger.error(f"Firecrawl API error ({response.status}): {error_text}")
                        raise Exception(f"Firecrawl API error ({response.status}): {error_text}")
                    
                    result = await response.json()
                    
                    if not result.get("success"):
                        error_msg = result.get('error', 'No error message provided')
                        self.logger.error(f"Firecrawl API response unsuccessful: {error_msg}")
                        raise Exception(f"Firecrawl API response unsuccessful: {error_msg}")
                    
                    # Extract screenshot data
                    screenshot_data = await self._extract_screenshot_data(session, result)
                    
                    # Save screenshot
                    await self._save_screenshot(screenshot_data, output_path)
                    
                    self.logger.info(f"Full-page screenshot saved: {output_path}")
                    return output_path
            except Exception as e:
                self.logger.error(f"Failed to capture full-page screenshot: {str(e)}")
                raise

    async def _extract_screenshot_data(self, session: aiohttp.ClientSession, result: Dict) -> bytes:
        """Extract screenshot data from Firecrawl API response"""
        try:
            # Handle different response formats for v1 API
            if "data" in result and "screenshot" in result["data"]:
                screenshot_data = result["data"]["screenshot"]
                if isinstance(screenshot_data, str):
                    if screenshot_data.startswith("http"):
                        async with session.get(screenshot_data) as screenshot_response:
                            if screenshot_response.status != 200:
                                raise Exception(f"Failed to download screenshot from {screenshot_data}: Status {screenshot_response.status}")
                            return await screenshot_response.read()
                    elif screenshot_data.startswith("data:image"):
                        # Handle base64 data URI
                        base64_string = screenshot_data.split(',')[1]
                        try:
                            return base64.b64decode(base64_string + "=" * (-len(base64_string) % 4))
                        except Exception as e:
                            raise Exception(f"Failed to decode base64 screenshot data: {str(e)}")
                    else:
                        # Try direct base64 decoding
                        try:
                            return base64.b64decode(screenshot_data + "=" * (-len(screenshot_data) % 4))
                        except Exception as e:
                            raise Exception(f"Failed to decode base64 screenshot: {str(e)}")
            
            # Fallback for actions-based screenshots
            if "data" in result and "actions" in result["data"] and "screenshots" in result["data"]["actions"]:
                screenshot_url = result["data"]["actions"]["screenshots"][0]
                async with session.get(screenshot_url) as screenshot_response:
                    if screenshot_response.status != 200:
                        raise Exception(f"Failed to download screenshot from {screenshot_url}: Status {screenshot_response.status}")
                    return await screenshot_response.read()
            
            raise Exception("No valid screenshot data or URL found in Firecrawl response")
        
        except Exception as e:
            self.logger.error(f"Error extracting screenshot data: {str(e)}")
            self.logger.debug(f"Firecrawl response: {json.dumps(result, indent=2)[:500]}...")
            raise

    async def _save_screenshot(self, screenshot_data: bytes, output_path: str):
        """Save screenshot data to file"""
        def write_file():
            with open(output_path, 'wb') as f:
                f.write(screenshot_data)
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, write_file)

    def get_input_schema(self) -> Dict[str, Any]:
        """Define the input schema for the full-page screenshot tool"""
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the website to capture full-page screenshot from"
                },
                "output_path": {
                    "type": "string",
                    "description": "Path where the full-page screenshot should be saved (optional, defaults to 'screenshots/screenshot.png')",
                    "default": "screenshots/screenshot.png"
                },
                "options": {
                    "type": "object",
                    "description": "Full-page screenshot options (fullPage is always enabled)",
                    "properties": {
                        "waitFor": {
                            "type": "integer",
                            "description": "Time to wait before taking screenshot in milliseconds (default: 3000 for full page load)",
                            "default": 3000
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "Total timeout for the request in milliseconds (default: 30000)",
                            "default": 30000
                        },
                        "mobile": {
                            "type": "boolean",
                            "description": "Whether to use mobile viewport (default: false for full desktop view)",
                            "default": False
                        }
                    }
                }
            },
            "required": ["url"]
        }

class ScreenshotAgent:
    """Google ADK Full-Page Screenshot Agent"""
    
    def __init__(self, config=None, model: str = None):
        from google.adk.models import Gemini
        
        self.config = config
        self.artifact_service = InMemoryArtifactService()
        self.screenshot_tool = ScreenshotTool(self.artifact_service)
        self.logger = self._setup_logger()
        
        # Determine the model to use
        if model is None:
            if config and hasattr(config, 'gemini_model'):
                model_name = getattr(config, 'gemini_model', "gemini-2.0-flash-exp")
            else:
                model_name = "gemini-2.0-flash-exp"
        else:
            model_name = model
        
        # Create Gemini model instance if config has API key
        if config and hasattr(config, 'gemini_api_key'):
            try:
                gemini_model = Gemini(
                    model=model_name,
                    api_key=getattr(config, 'gemini_api_key')
                )
                model_to_use = gemini_model
            except Exception as e:
                self.logger.warning(f"Failed to create Gemini model with API key: {e}")
                model_to_use = model_name
        else:
            model_to_use = model_name
        
        # Create the ADK agent with enhanced full-page screenshot instructions
        self.agent = LlmAgent(
            name="fullpage_screenshot_agent",
            model=model_to_use,
            instruction="""
            You are a full-page screenshot capture agent. Your primary function is to capture complete, 
            full-page screenshots of websites using the Firecrawl API through the screenshot tool.
            
            Key capabilities:
            - Always capture FULL-PAGE screenshots (entire webpage content)
            - Optimize for complete page loading before capture
            - Handle long pages and dynamic content
            - Provide high-quality screenshots suitable for analysis
            
            When asked to capture a screenshot:
            1. Use the screenshot_tool with the provided URL
            2. Always ensure fullPage=True for complete page capture
            3. Allow sufficient wait time for full page loading (default 3000ms)
            4. Optionally specify output path and enhanced screenshot options
            5. Save the screenshot as an artifact
            6. Provide clear information about the full-page screenshot capture
            
            Always emphasize that screenshots are captured as full-page, showing the complete webpage content.
            Be helpful and provide clear information about the screenshot capture process and results.
            """,
            description="An agent specialized in capturing full-page website screenshots using Firecrawl API with optimized settings for complete page capture",
            tools=[self.screenshot_tool]
        )
        
        # Create runner for the agent
        self.runner = InMemoryRunner(agent=self.agent)

    def _setup_logger(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        return logging.getLogger(self.__class__.__name__)

    async def capture_screenshot(self, url: str, output_path: str = None, options: Dict = None) -> str:
        """Capture full-page screenshot using the screenshot tool directly"""
        try:
            if output_path is None:
                output_path = "screenshots/fullpage_screenshot.png"
            
            # Ensure full-page options are set
            full_page_options = options or {}
            full_page_options.update({
                "waitFor": full_page_options.get("waitFor", 3000),
                "timeout": full_page_options.get("timeout", 30000)
            })
            
            # Call the tool directly with a mock ToolContext
            from types import SimpleNamespace
            mock_context = SimpleNamespace()
            
            tool_result = await self.screenshot_tool.execute(
                context=mock_context,
                url=url,
                output_path=output_path,
                options=full_page_options
            )
            
            if not tool_result.get("success"):
                raise Exception(tool_result.get("error", "Full-page screenshot capture failed"))
            
            return tool_result["result"]["screenshot_path"]
            
        except Exception as e:
            self.logger.error(f"Full-page screenshot capture failed: {str(e)}")
            raise

    async def capture_full_page_url(self, url: str, output_path: str) -> str:
        """Capture full-page screenshot for a URL, used by pipeline endpoint"""
        return await self.capture_screenshot(
            url, 
            output_path, 
            options={
                "waitFor": 3000,
                "timeout": 30000
            }
        )

    async def capture_multiple_screenshots(self, urls: list, base_output_dir: str = "screenshots") -> Dict[str, Any]:
        """Capture full-page screenshots for multiple URLs"""
        results = []
        
        for i, url in enumerate(urls):
            try:
                output_path = f"{base_output_dir}/fullpage_screenshot_{i+1}.png"
                result_path = await self.capture_screenshot(
                    url, 
                    output_path,
                    options={"waitFor": 3000, "timeout": 30000}
                )
                results.append({
                    "url": url,
                    "output_path": result_path,
                    "screenshot_type": "full-page",
                    "success": True,
                    "error": None
                })
                self.logger.info(f"Full-page screenshot captured for {url}")
            except Exception as e:
                self.logger.error(f"Failed to capture full-page screenshot for {url}: {str(e)}")
                results.append({
                    "url": url,
                    "screenshot_type": "full-page",
                    "success": False,
                    "error": str(e)
                })
        
        successful_count = len([r for r in results if r["success"]])
        failed_count = len([r for r in results if not r["success"]])
        
        self.logger.info(f"Batch full-page screenshot capture completed: {successful_count} successful, {failed_count} failed")
        
        return {
            "success": True,
            "results": results,
            "total_processed": len(urls),
            "successful": successful_count,
            "failed": failed_count,
            "screenshot_type": "full-page"
        }

    def get_agent(self) -> LlmAgent:
        """Get the underlying ADK agent"""
        return self.agent

    def get_runner(self) -> InMemoryRunner:
        """Get the runner instance"""
        return self.runner