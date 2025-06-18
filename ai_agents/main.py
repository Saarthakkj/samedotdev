# AI Website Cloning System
# Core implementation with Agent Development Kit (ADK) integration

import asyncio
import json
import re
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import base64
import hashlib
import logging
from agents.analyzer_agent import AnalyzerAgent
from agents.generator_agent import GeneratorAgent

# from dotenv import load_dotenv
# load_dotenv(".env" , __dirname = os.path)  

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
    
    # Example log with extra fields (similar to your AnalyzerAgent)
    logger = logging.getLogger("AnalyzerAgent")
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
    gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
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

class LLMRequest(BaseModel):
    system_prompt: str
    #  e.g. [{ "role": "user", "content": "Hello" }, ...]
    messages: List[dict]

class LLMResult(BaseModel):
    response: str

@app.post("/generate", response_model=LLMResult)
async def generate_llm_answer(req: LLMRequest):
    """
    Forward system prompt + messages to Gemini via GeneratorAgent (or directly).
    Return plain text exactly like ai-sdk generateText() did.
    """
    
    # Parse URL from messages
    url = None
    for message in req.messages:
        if message.get('role') == 'user':
            content = message.get('content', '')
            # Look for URL patterns in the content
            import re
            url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
            urls = re.findall(url_pattern, content)
            if urls:
                url = urls[0]  # Take the first URL found
                break
    
    if not url:
        raise HTTPException(status_code=400, detail="No URL found in messages")
    
    
    analyzer = AnalyzerAgent(config)
    generator = GeneratorAgent(config)
    
    analysis_result = await analyzer.analyze_screenshot(url , req.system_prompt)
    generated_code = await generator.generate_code(analysis_result , req.system_prompt)
    
    print(f"this is the analysis result of GENERATED CODE : \n\n{generated_code} \n\n")
    
    return LLMResult(response=json.dumps(generated_code))
    
    
    
    #   run this when agnets after generator agents are done : 
    
    
    
    
    # clone_website(url  , req.system_prompt, "react" , {}) 
    
    
    
    # try:
    #     prompt_text = req.system_prompt + "\n\n" + "\n".join(
    #         f"{m['role']}: {m['content']}" for m in req.messages
    #     )
    #     # reuse your existing GeneratorAgent OR call the model here
    #     model = genai.GenerativeModel("gemini-2.0-flash-exp")
    #     resp = await model.generate_content_async(prompt_text)
    #     return LLMResult(response=resp.text.strip())
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    
    # Ensure output directory exists
    os.makedirs(config.output_dir, exist_ok=True)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)