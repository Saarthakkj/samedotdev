
from google.adk.agents import Agent as ADKAgent  # type: ignore

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional
import asyncio
import google.generativeai as genai
from config.system_config import SystemConfig
import os

class GeneratorAgent(ADKAgent):
    # Pydantic field
    _config: SystemConfig = None

    def __init__(self, config: SystemConfig):
        
        
        super().__init__(
            name="generator_agent",
            model="gemini-2.0-flash-exp",
            description="Generates website code based on analysis.",
            instruction="Generate website code based on analysis.",
            tools=[],
        )
        object.__setattr__(self , "_config" , config)
        object.__setattr__(self , "logger" , self._setup_logger())
        # Initialize Gemini API
        if self._config.gemini_api_key :
            self.logger.info("Using Gemini API key for generation")
            genai.configure(api_key=self._config.gemini_api_key)
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

    async def generate_code(self, analysis: Dict, system_prompt: str) -> Dict:
        """
        Generate code based on analysis - this is the method your orchestrator is calling
        This is an alias for generate_website to maintain compatibility
        """
        return await self.generate_website(analysis , system_prompt)

    async def generate_website(self, analysis: Dict , system_prompt : str = "")   -> Dict:
        """Generate website based on analysis using Gemini"""
        # self.logger.info(f"Starting website generation for output directory: {output_dir}")
        
    
        if not analysis or not isinstance(analysis, dict):
            self.logger.error("Invalid analysis provided")
            raise ValueError("Invalid analysis structure")

        
        # Generate project structure and code
        generated_files = await self._generate_project_files(analysis , system_prompt)

        result = {
            "status": "success",
            "code" : generated_files
        }
        self.logger.info(f"Website generation completed successfully")
        return result

      
    async def _generate_project_files(self, analysis: Dict, system_prompt: str) ->  str:
        """Generate all project files based on analysis"""
        # generated_files = {}
        
        print(f"this is the analysis : \n\n{analysis} \n\n")
        
        analysis_json = json.dumps(analysis , indent =2 , ensure_ascii=False)
        
        # Create prompt based on analysis
        
        prompt = [system_prompt.strip() ,  analysis_json] 
        # prompt = self._create_generation_prompt(analysis)
        
        try:
            # Generate code using Gemini
            response = await self.model.generate_content_async(prompt)
            
            if not response or not response.text:
                raise ValueError("Empty response from Gemini")
            
            
            print(f"this is the response from gemini  -- inside generation agent : \n\n{response.text} \n\n")
            
            return response.text

        except Exception as e:
            self.logger.error(f"Failed to generate project files: {str(e)}")
            raise
