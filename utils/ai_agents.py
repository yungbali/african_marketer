from anthropic import Anthropic
from typing import Dict, List, Optional
import json

class AfricanMusicAIAgent:
    def __init__(self, anthropic_key: str):
        """Initialize the AI agent with the Anthropic API key."""
        self.client = Anthropic(api_key=anthropic_key)
        self.conversation_history: List[Dict] = []
        self.system_prompt = """You are an expert in African music marketing and industry analysis. 
        Your role is to provide clear, actionable advice based on current industry trends and best practices."""

    def get_advice(self, prompt: str) -> Dict:
        """Get advice from Claude based on the prompt."""
        try:
            # Create messages list (without system message)
            messages = []
            
            # Add conversation history
            for msg in self.conversation_history:
                if msg["role"] in ["user", "assistant"]:  # Only include user and assistant messages
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Add current prompt
            messages.append({
                "role": "user",
                "content": prompt
            })

            # Get response from Claude using the correct API parameters
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                messages=messages,
                system=self.system_prompt,  # System prompt goes here
                max_tokens=1000,
                temperature=0.7
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