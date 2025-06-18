# from config.system_config import SystemConfig
# from pathlib import Path
# import logging
# import requests
# import base64
# from typing import Dict, Optional
# import asyncio
# import aiohttp
# import os

# class ScreenshotAgent:
#     def __init__(self, config: SystemConfig):
#         self.config = config
#         self.logger = self._setup_logger()
#         self.firecrawl_api_key = os.getenv('FIRECRAWL_API_KEY')
#         self.firecrawl_base_url = "https://api.firecrawl.dev"
        
#         if not self.firecrawl_api_key:
#             self.logger.warning("Firecrawl API key not found in environment")

#     def _setup_logger(self):
#         logging.basicConfig(level=logging.INFO)
#         return logging.getLogger(self.__class__.__name__)

#     async def capture_full_page(self, page, output_path: str) -> str:
#         """
#         Capture full page screenshot using current page URL
#         This method extracts the URL from the page object and uses Firecrawl
#         """
#         try:
#             current_url = page.url
#             return await self.capture_full_page_url(current_url, output_path)
#         except Exception as e:
#             self.logger.error(f"Failed to capture screenshot from page {page.url}: {str(e)}")
#             raise

#     async def capture_full_page_url(self, url: str, output_path: str) -> str:
#         """Capture full page screenshot using Firecrawl API"""
#         try:
#             Path(output_path).parent.mkdir(parents=True, exist_ok=True)
#             screenshot_data = await self._firecrawl_screenshot(url)
#             await self._save_screenshot(screenshot_data, output_path)
#             self.logger.info(f"Screenshot saved using Firecrawl: {output_path}")
#             return output_path
#         except Exception as e:
#             self.logger.error(f"Firecrawl screenshot failed for URL {url}: {str(e)}")
#             raise

#     async def _firecrawl_screenshot(self, url: str) -> bytes:
#         """Make async request to Firecrawl API for screenshot"""
#         if not self.firecrawl_api_key:
#             raise ValueError("Firecrawl API key is required")

#         headers = {
#             "Authorization": f"Bearer {self.firecrawl_api_key}",
#             "Content-Type": "application/json"
#         }
        
#         payload = {
#             "url": url,
#             "formats": ["screenshot"],
#             "actions": [
#                 {"type": "wait", "milliseconds": 2000},
#                 {"type": "screenshot"}
#             ]
#         }

#         async with aiohttp.ClientSession() as session:
#             async with session.post(
#                 f"{self.firecrawl_base_url}/v1/scrape",
#                 headers=headers,
#                 json=payload
#             ) as response:
#                 if response.status != 200:
#                     error_text = await response.text()
#                     self.logger.error(f"Firecrawl API error ({response.status}): {error_text}")
#                     raise Exception(f"Firecrawl API error ({response.status}): {error_text}")
                
#                 result = await response.json()
                
#                 if not result.get("success"):
#                     self.logger.error(f"Firecrawl API response unsuccessful: {result}")
#                     raise Exception(f"Firecrawl API response unsuccessful: {result.get('error', 'No error message provided')}")
                
#                 # First check for screenshot URL in data.actions.screenshots
#                 if "data" in result and "actions" in result["data"] and "screenshots" in result["data"]["actions"]:
#                     screenshot_url = result["data"]["actions"]["screenshots"][0]
#                     async with session.get(screenshot_url) as screenshot_response:
#                         if screenshot_response.status != 200:
#                             self.logger.error(f"Failed to download screenshot from {screenshot_url}: {screenshot_response.status}")
#                             raise Exception(f"Failed to download screenshot from {screenshot_url}")
#                         return await screenshot_response.read()
                
#                 # Then check for screenshot in data.screenshot (base64)
#                 elif "data" in result and "screenshot" in result["data"]:
#                     screenshot_data = result["data"]["screenshot"]
#                     # If it's a URL, download it
#                     if isinstance(screenshot_data, str) and screenshot_data.startswith("http"):
#                         async with session.get(screenshot_data) as screenshot_response:
#                             if screenshot_response.status != 200:
#                                 self.logger.error(f"Failed to download screenshot from {screenshot_data}: {screenshot_response.status}")
#                                 raise Exception(f"Failed to download screenshot from {screenshot_data}")
#                             return await screenshot_response.read()
#                     # If it's base64, decode it
#                     elif isinstance(screenshot_data, str):
#                         try:
#                             # Ensure proper padding
#                             screenshot_base64 = screenshot_data + "=" * (-len(screenshot_data) % 4)
#                             return base64.b64decode(screenshot_base64)
#                         except Exception as e:
#                             self.logger.error(f"Failed to decode base64 screenshot: {str(e)}, Response: {result}")
#                             raise Exception(f"Failed to decode base64 screenshot: {str(e)}")
                
#                 self.logger.error(f"No screenshot data or URL returned from Firecrawl: {result}")
#                 raise Exception("No screenshot data or URL returned from Firecrawl")

#     async def _save_screenshot(self, screenshot_data: bytes, output_path: str):
#         """Save screenshot data to file"""
#         def write_file():
#             with open(output_path, 'wb') as f:
#                 f.write(screenshot_data)
        
#         loop = asyncio.get_event_loop()
#         await loop.run_in_executor(None, write_file)

#     def capture_full_page_sync(self, url: str, output_path: str) -> str:
#         """Synchronous version using requests (fallback)"""
#         try:
#             if not self.firecrawl_api_key:
#                 raise ValueError("Firecrawl API key is required")

#             Path(output_path).parent.mkdir(parents=True, exist_ok=True)

#             headers = {
#                 "Authorization": f"Bearer {self.firecrawl_api_key}",
#                 "Content-Type": "application/json"
#             }
            
#             payload = {
#                 "url": url,
#                 "formats": ["screenshot"],
#                 "actions": [
#                     {"type": "wait", "milliseconds": 2000},
#                     {"type": "screenshot"}
#                 ]
#             }

#             response = requests.post(
#                 f"{self.firecrawl_base_url}/v1/scrape",
#                 headers=headers,
#                 json=payload
#             )
            
#             if response.status_code != 200:
#                 self.logger.error(f"Firecrawl API error ({response.status_code}): {response.text}")
#                 raise Exception(f"Firecrawl API error ({response.status_code}): {response.text}")
            
#             result = response.json()
            
#             if not result.get("success"):
#                 self.logger.error(f"Firecrawl API response unsuccessful: {result}")
#                 raise Exception(f"Firecrawl API response unsuccessful: {result.get('error', 'No error message provided')}")
            
#             # First check for screenshot URL in data.actions.screenshots
#             if "data" in result and "actions" in result["data"] and "screenshots" in result["data"]["actions"]:
#                 screenshot_url = result["data"]["actions"]["screenshots"][0]
#                 screenshot_response = requests.get(screenshot_url)
#                 if screenshot_response.status_code != 200:
#                     self.logger.error(f"Failed to download screenshot from {screenshot_url}: {screenshot_response.status_code}")
#                     raise Exception(f"Failed to download screenshot from {screenshot_url}")
#                 screenshot_data = screenshot_response.content
            
#             # Then check for screenshot in data.screenshot (base64 or URL)
#             elif "data" in result and "screenshot" in result["data"]:
#                 screenshot_data = result["data"]["screenshot"]
#                 # If it's a URL, download it
#                 if isinstance(screenshot_data, str) and screenshot_data.startswith("http"):
#                     screenshot_response = requests.get(screenshot_data)
#                     if screenshot_response.status_code != 200:
#                         self.logger.error(f"Failed to download screenshot from {screenshot_data}: {screenshot_response.status_code}")
#                         raise Exception(f"Failed to download screenshot from {screenshot_data}")
#                     screenshot_data = screenshot_response.content
#                 # If it's base64, decode it
#                 elif isinstance(screenshot_data, str):
#                     try:
#                         # Ensure proper padding
#                         screenshot_base64 = screenshot_data + "=" * (-len(screenshot_data) % 4)
#                         screenshot_data = base64.b64decode(screenshot_base64)
#                     except Exception as e:
#                         self.logger.error(f"Failed to decode base64 screenshot: {str(e)}, Response: {result}")
#                         raise Exception(f"Failed to decode base64 screenshot: {str(e)}")
            
#             else:
#                 self.logger.error(f"No screenshot data or URL returned from Firecrawl: {result}")
#                 raise Exception("No screenshot data or URL returned from Firecrawl")
            
#             with open(output_path, 'wb') as f:
#                 f.write(screenshot_data)
            
#             self.logger.info(f"Screenshot saved using Firecrawl (sync): {output_path}")
#             return output_path
            
#         except Exception as e:
#             self.logger.error(f"Firecrawl screenshot failed (sync) for URL {url}: {str(e)}")
#             raise

#     async def capture_with_options(self, url: str, output_path: str, **screenshot_options) -> str:
#         """Capture screenshot with custom Firecrawl options"""
#         try:
#             Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
#             if not self.firecrawl_api_key:
#                 raise ValueError("Firecrawl API key is required")

#             headers = {
#                 "Authorization": f"Bearer {self.firecrawl_api_key}",
#                 "Content-Type": "application/json"
#             }
            
#             default_wait_time = 2000
#             wait_time = screenshot_options.get("waitFor", default_wait_time)
            
#             payload = {
#                 "url": url,
#                 "formats": ["screenshot"],
#                 "actions": [
#                     {"type": "wait", "milliseconds": wait_time},
#                     {"type": "screenshot"}
#                 ]
#             }

#             async with aiohttp.ClientSession() as session:
#                 async with session.post(
#                     f"{self.firecrawl_base_url}/v1/scrape",
#                     headers=headers,
#                     json=payload
#                 ) as response:
#                     if response.status != 200:
#                         error_text = await response.text()
#                         self.logger.error(f"Firecrawl API error ({response.status}): {error_text}")
#                         raise Exception(f"Firecrawl API error ({response.status}): {error_text}")
                    
#                     result = await response.json()
                    
#                     if not result.get("success"):
#                         self.logger.error(f"Firecrawl API response unsuccessful: {result}")
#                         raise Exception(f"Firecrawl API response unsuccessful: {result.get('error', 'No error message provided')}")
                    
#                     # Check for screenshot in data.screenshot (base64)
#                     if "data" in result and "screenshot" in result["data"]:
#                         screenshot_base64 = result["data"]["screenshot"]
#                         try:
#                             if not isinstance(screenshot_base64, str) or not screenshot_base64:
#                                 raise ValueError("Screenshot data is not a valid base64 string")
#                             screenshot_base64 = screenshot_base64 + "=" * (-len(screenshot_base64) % 4)
#                             screenshot_data = base64.b64decode(screenshot_base64)
#                         except Exception as e:
#                             self.logger.error(f"Failed to decode base64 screenshot: {str(e)}, Response: {result}")
#                             raise Exception(f"Failed to decode base64 screenshot: {str(e)}")
                    
#                     # Check for screenshot URL in data.actions.screenshots
#                     elif "data" in result and "actions" in result["data"] and "screenshots" in result["data"]["actions"]:
#                         screenshot_url = result["data"]["actions"]["screenshots"][0]
#                         async with session.get(screenshot_url) as screenshot_response:
#                             if screenshot_response.status != 200:
#                                 self.logger.error(f"Failed to download screenshot from {screenshot_url}: {screenshot_response.status}")
#                                 raise Exception(f"Failed to download screenshot from {screenshot_url}")
#                             screenshot_data = await screenshot_response.read()
                    
#                     else:
#                         self.logger.error(f"No screenshot data or URL returned from Firecrawl: {result}")
#                         raise Exception("No screenshot data or URL returned from Firecrawl")
                    
#                     await self._save_screenshot(screenshot_data, output_path)
                    
#             self.logger.info(f"Screenshot with custom options saved: {output_path}")
#             return output_path
            
#         except Exception as e:
#             self.logger.error(f"Firecrawl screenshot with options failed for URL {url}: {str(e)}")
#             raise