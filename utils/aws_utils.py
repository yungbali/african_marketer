import boto3
from botocore.exceptions import ClientError
import logging
import json
import os

logger = logging.getLogger(__name__)

class BedrockClients:
    def __init__(self, region_name: str = "us-east-1"):
        """Initialize Bedrock clients with basic IAM credentials"""
        # Get basic credentials
        access_key = os.getenv('AWS_ACCESS_KEY_ID')
        secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        
        if not access_key or not secret_key:
            raise ValueError(
                "Missing required AWS credentials: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY "
                "must be set in your environment variables."
            )
        
        # Initialize clients with basic credentials
        self.bedrock = boto3.client(
            "bedrock",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region_name
        )
        
        self.runtime = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region_name
        )

    def invoke_model(self, prompt: str, model_id: str, max_tokens: int = 1000, temperature: float = 0.7):
        """Invoke the Claude model with the given prompt."""
        try:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature
            }
            
            response = self.runtime.invoke_model(
                modelId=model_id,
                body=json.dumps(body)
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except Exception as e:
            logger.error(f"Error invoking model: {str(e)}")
            raise