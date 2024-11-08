from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
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
            # Create the complete message
            full_prompt = f"{self.system_prompt}\n\nCurrent conversation:\n"
            for msg in self.conversation_history:
                full_prompt += f"{msg['role']}: {msg['content']}\n"
            full_prompt += f"\nUser: {prompt}"

            # Get response from Claude
            response = self.client.completions.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0.7,
                prompt=full_prompt
            )

            # Extract the response content
            advice = response.completion

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