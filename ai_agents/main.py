# AI Website Cloning System
# Core implementation with Agent Development Kit (ADK) integration

import asyncio
import json
import re
import os
import base64
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import base64
import hashlib
import logging
from agents.analyzer_agent import AnalyzerAgent
from agents.generator_agent import GeneratorAgent

import aiohttp
# # Core dependencies

import google.generativeai as genai
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import requests
from pathlib import Path

# FastAPI for API wrapper
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from logging.handlers import RotatingFileHandler
from config.system_config import SystemConfig, CloneRequest, CloneResult
from agents.website_clone import WebsiteCloneOrchestrator

# --- Firecrawl SDK -----------------------------------------------------
# We call the synchronous SDK in a thread-pool so the async event-loop is
# not blocked.
from firecrawl import FirecrawlApp, ScrapeOptions


def scrape_with_ssl_fallback(app , url, formats=['screenshot']):
    """
    Attempt to scrape with SSL verification first, 
    then fallback to skipping SSL verification if it fails
    """
    try:
        # First attempt with SSL verification
        print("Attempting scrape with SSL verification...")
        scrape_result = app.scrape_url(
            url,
            formats=formats
        )
        print("✅ Scrape successful with SSL verification")
        return scrape_result
        
    except Exception as e:
        if "SSL error" in str(e) or "TLS" in str(e):
            print("⚠️ SSL error detected, retrying without TLS verification...")
            try:
                # Retry without SSL verification
                scrape_result = app.scrape_url(
                    url,
                    formats=formats,
                    skip_tls_verification=True
                )
                print("✅ Scrape successful without SSL verification")
                return scrape_result
            except Exception as retry_error:
                print(f"❌ Scrape failed even without SSL verification: {retry_error}")
                raise retry_error
        else:
            print(f"❌ Non-SSL related error: {e}")
            raise e

# # Usage
# try:
#     result = scrape_with_ssl_fallback('https://problematic-ssl-site.com')
#     print("Content:", result.markdown[:200] + "...")
# except Exception as e:
#     print(f"Final error: {e}")

async def _capture_full_page_url(url: str, output_path: str) -> str:
        """
        Capture a full-page screenshot of `url` using the Firecrawl API and save
        it to `output_path`.
        """
        # logger for this helper
        logger = logging.getLogger("firecrawl_helper")
        logger.info(f"Starting screenshot capture for URL: {url}")

        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            logger.error("FIRECRAWL_API_KEY environment variable not set")
            raise ValueError("FIRECRAWL_API_KEY environment variable not set")

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Created output directory for path: {output_path}")

        
        app = FirecrawlApp(api_key=api_key)

        # ─────────────────────────────────────────────────────────────
        # Firecrawl call with longer timeout + automatic retries
        # ─────────────────────────────────────────────────────────────
        MAX_RETRIES = 10
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                scrape_result = scrape_with_ssl_fallback(app , url)
                break  # 👍 success – exit retry-loop
            except Exception as e:
                logger.warning(
                    f"Firecrawl scrape_url timeout (attempt {attempt}/{MAX_RETRIES}): {e}"
                )
                if attempt == MAX_RETRIES:
                    raise                # bubble up on final failure
                await asyncio.sleep(2 ** attempt)  # exponential back-off

        # Access the screenshot (could be bytes, base-64 string, or URL)
        screenshot_data = scrape_result.screenshot
        
        if not screenshot_data:
            logger.error("No screenshot data returned from Firecrawl")
            raise Exception("No screenshot data returned from Firecrawl")

        # ------------------------------------------------------------------
        # Normalise → img_bytes (bytes)  -----------------------------------
        # ------------------------------------------------------------------
        img_bytes: bytes

        if isinstance(screenshot_data, (bytes, bytearray)):
            # Case 1: already raw bytes
            img_bytes = bytes(screenshot_data)

        elif isinstance(screenshot_data, str):
            # Case 2 / 3: string → could be URL or base-64
            if screenshot_data.startswith("http"):
                # Public URL, fetch it
                logger.debug("Screenshot returned as URL — downloading …")
                resp = requests.get(screenshot_data, timeout=20)
                resp.raise_for_status()
                img_bytes = resp.content
            else:
                # Base-64 string (may contain data-URL prefix & missing padding)
                logger.debug("Screenshot returned as base-64 string — decoding …")
                # Remove optional data-URL header
                if "," in screenshot_data and screenshot_data.startswith("data"):
                    screenshot_data = screenshot_data.split(",", 1)[1]

                # Fix padding (length must be multiple of 4)
                padding = (-len(screenshot_data)) % 4
                if padding:
                    screenshot_data += "=" * padding

                img_bytes = base64.b64decode(screenshot_data)

        else:
            raise TypeError("Unsupported screenshot data type "
                            f"{type(screenshot_data)}")

        # Save file in executor to avoid blocking the event-loop
        loop = asyncio.get_event_loop()

        def _write():
            with open(output_path, "wb") as fp:
                fp.write(img_bytes)
            logger.debug(f"Screenshot data written to file: {output_path}")

        await loop.run_in_executor(None, _write)
        logger.info(f"Screenshot successfully saved to: {output_path}")

        return output_path

def setup_logging(log_file: str = "website_clone.log", log_level: int = logging.INFO) -> None:
    """
    Configure logging to capture all events, including custom 'extra' fields, during the website cloning process.

    Args:
        log_file (str): Path to the log file.
        log_level (int): Logging level (e.g., logging.INFO, logging.DEBUG).
    """
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Prevent duplicate logs if setup is called multiple times
    if logger.handlers:
        logger.handlers.clear()

    # Custom formatter to include extra fields
    class CustomFormatter(logging.Formatter):
        def format(self, record):
            # Default format for standard fields
            base_format = '%(asctime)s:%(name)s:%(levelname)s:%(message)s'
            # Add extra fields if they exist
            extra_fields = [
                f"{key}={value}"
                for key, value in sorted(record.__dict__.items())
                if key in ['framework', 'components_count', 'layout_type']
            ]
            if extra_fields:
                base_format += ' ' + ' '.join(extra_fields)
            self._style._fmt = base_format
            return super().format(record)

    # Create format for log messages
    formatter = CustomFormatter(datefmt='%Y-%m-%d %H:%M:%S')

    # Console handler for printing to stdout
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler with rotation (max 5MB, keep 3 backups)
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

# Example usage in your AnalyzerAgent or main script
if __name__ == "__main__":
    # Set up logging
    setup_logging()
    
    logger = logging.getLogger("Logger")
    analysis = {
        "framework": {"primary": "React"},
        "components": ["navigation", "hero", "footer"],
        "layout": {"type": "modern"}
    }
    logger.info("Website analysis completed successfully", extra={
        "framework": analysis.get("framework", {}).get("primary", "unknown"),
        "components_count": len(analysis.get("components", [])),
        "layout_type": analysis.get("layout", {}).get("type", "unknown")
    })

# FastAPI Application
app = FastAPI(title="AI Website Cloning System", version="1.0.0")

# Global config (would be loaded from environment)
config = SystemConfig(
    gemini_api_key=os.getenv("GOOGLE_GENERATIVE_AI_API_KEY", ""),
    firecrawl_api_key=os.getenv("FIRECRAWL_API_KEY", "")
)

@app.post("/clone", response_model=CloneResult)
async def clone_website(request: CloneRequest):
    """Clone a website endpoint"""
    try:
        orchestrator = WebsiteCloneOrchestrator(config)
        return await orchestrator.clone_website(
            request.url, 
            request.framework, 
            request.options
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI Website Cloning System",
        "version": "1.0.0",
        "endpoints": {
            "clone": "POST /clone",
            "health": "GET /health"
        }
    }
    
class Message(BaseModel):
    role: str
    content: str

class LLMRequest(BaseModel):
    messages : List[Message]

class LLMResult(BaseModel):
    response: str

@app.post("/generate", response_model=LLMResult)
async def generate_llm_answer(req : LLMRequest):
    
    messages = req.messages
    
    user_prompt = messages[-1].content
    
    
    # print("this is request : \n\n\n" , req[len(req)-1] , "\n\n\n")
    # print(f"this is the prompt : \n\n\n\n{messages} \n\n\n\n")
    # print(f"this is user prompt :  \n\n\n{user_prompt}\n\n")
    # print(f"this is length of messages : \n\n{len(messages)}\n\n of  messages (<- req.messages) : \n\n{messages}\n\n ")
    sys_prompt = messages[0].content + "\n\n" + messages[1].content
    # print("sys prompt :" , sys_prompt)

    
    # prompt = req.messages[len(req.messages)-1]['content'][:1000]
    """
    Forward system prompt + messages to Gemini via GeneratorAgent (or directly).
    Return plain text exactly like ai-sdk generateText() did.
    """
    
    # Parse URL from messages
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(url_pattern, user_prompt)
    url  = urls[0] if urls else None

    if not url:
        raise HTTPException(status_code=400, detail="No URL found in messages")
    
    print(f"this is the url and config : \n\n{url}  {config} \n\n")    
    
    analyzer = AnalyzerAgent(config)
    generator = GeneratorAgent(config)
    await _capture_full_page_url(url , "output.png")
    analysis_result = await analyzer.analyze_screenshot("output.png")
    generated_code = await generator.generate_code(analysis_result , sys_prompt)
    
    # print(f"this is the analysis result of GENERATED CODE : \n\n{generated_code} \n\n")
    
    return LLMResult(response=json.dumps(generated_code))
    
if __name__ == "__main__":
    import uvicorn
    
    # Ensure output directory exists
    os.makedirs(config.output_dir, exist_ok=True)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)