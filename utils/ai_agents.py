"""Configuration settings for the application."""

# AWS Configuration
AWS_CONFIG = {
    "region_name": "us-east-1",
    "model_id": "anthropic.claude-3-sonnet-20240229-v1:0",
    "max_tokens": 1000,
    "temperature": 0.7
}

# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "standard"
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard"
        }
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "INFO",
        }
    }
}

# Streamlit Configuration
STREAMLIT_CONFIG = {
    "page_title": "African Music Marketing Assistant",
    "page_icon": "🎵",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

import boto3
import json
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class AfricanMusicAIAgent:
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime')
        self.model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

    def get_advice(self, prompt, context):
        try:
            # Format context into string
            context_str = "\n".join([f"{k}: {v}" for k,v in context.items()])
            
            # Create the conversation messages
            conversation = [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": f"As an AI expert in African music marketing and promotion, please provide advice based on this context:\n\n{context_str}\n\nQuestion: {prompt}"
                        }
                    ]
                }
            ]

            # Use the converse API
            response = self.bedrock.converse(
                modelId=self.model_id,
                messages=conversation,
                inferenceConfig={
                    "maxTokens": 4096,
                    "temperature": 0.7
                }
            )
            
            # Extract response text
            response_text = response["output"]["message"]["content"][0]["text"]
            
            return {
                "status": "success",
                "advice": response_text
            }
                
        except Exception as e:
            logger.error(f"Error getting advice: {str(e)}")
            return {
                "status": "error", 
                "advice": f"I'm currently experiencing technical difficulties: {str(e)}"
            }