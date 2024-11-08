from anthropic import Anthropic
from typing import Dict, List, Optional
import json
import os

class AfricanMusicAIAgent:
    def __init__(self, anthropic_key: str):
        """Initialize the AI agent with the Anthropic API key."""
        self.client = Anthropic(api_key=anthropic_key)
        self.conversation_history: List[Dict] = []
        self.system_prompt = """You are an expert in African music marketing and industry analysis. 
        Your role is to provide clear, actionable advice based on current industry trends and best practices.
        
        Key areas of expertise:
        - EPK (Electronic Press Kit) development
        - Digital marketing strategies
        - Music industry trends
        - Artist branding
        - Social media strategy
        - Music distribution in African markets
        
        Always provide specific, actionable advice with examples when possible."""

    def get_advice(self, prompt: str) -> Dict:
        """Get advice from Claude based on the prompt."""
        try:
            # Create messages list with system prompt and conversation history
            messages = [
                {
                    "role": "assistant",
                    "content": self.system_prompt
                }
            ]
            
            # Add conversation history
            messages.extend(self.conversation_history)
            
            # Add current prompt
            messages.append({
                "role": "user",
                "content": prompt
            })

            # Get response from Claude
            response = self.client.messages.create(
                model="claude-3-opus-20240229",  # Using latest Claude 3 model
                max_tokens=1000,
                temperature=0.7,
                messages=messages
            )

            # Extract the response content
            advice = response.content[0].text

            # Update conversation history
            self.conversation_history.append({"role": "user", "content": prompt})
            self.conversation_history.append({"role": "assistant", "content": advice})

            # Keep conversation history manageable
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]

            return {
                "status": "success",
                "advice": advice
            }

        except Exception as e:
            return {
                "status": "error",
                "advice": f"Error: {str(e)}"
            }

    def clear_conversation(self) -> Dict:
        """Clear the conversation history."""
        try:
            self.conversation_history = []
            return {
                "status": "success",
                "message": "Conversation cleared successfully."
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to clear conversation: {str(e)}"
            }