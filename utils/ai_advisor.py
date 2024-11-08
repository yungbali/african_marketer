from typing import Dict, List, Optional
import openai
from datetime import datetime
import pandas as pd
from pathlib import Path
import docx
import PyPDF2
import json

class AIAdvisor:
    def __init__(self, openai_key: str):
        self.openai_client = openai.OpenAI(api_key=openai_key)
        self.conversation_history = []
        self.uploaded_docs = {}
        
    def process_document(self, file, filename: str) -> Dict:
        """Process uploaded documents and extract content"""
        content = ""
        file_type = Path(filename).suffix.lower()
        
        if file_type == '.pdf':
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                content += page.extract_text()
        elif file_type in ['.doc', '.docx']:
            doc = docx.Document(file)
            content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        elif file_type == '.txt':
            content = file.read().decode('utf-8')
        
        self.uploaded_docs[filename] = {
            'content': content,
            'uploaded_at': datetime.now().isoformat(),
            'type': file_type
        }
        
        return {'status': 'success', 'message': f'Processed {filename}'}

    async def get_advice(self, query: str, context: Optional[Dict] = None) -> Dict:
        """Get AI advice based on query and context"""
        
        # Build the context prompt
        context_prompt = ""
        if context:
            context_prompt += f"\nMarket Context: {json.dumps(context)}\n"
        
        # Add document context if referenced
        if "document" in query.lower() or "file" in query.lower():
            context_prompt += "\nUploaded Documents:\n"
            for filename, doc in self.uploaded_docs.items():
                context_prompt += f"\n{filename} content:\n{doc['content'][:1000]}..."

        messages = [
            {"role": "system", "content": """You are an expert AI advisor for the African music industry. 
             You provide advice based on market data, cultural context, and industry best practices.
             Always consider cultural authenticity and ethical implications in your recommendations."""},
            {"role": "user", "content": f"{context_prompt}\n\nQuery: {query}"}
        ]
        
        # Add relevant conversation history
        messages.extend(self.conversation_history[-5:])  # Last 5 exchanges
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7
        )
        
        advice = response.choices[0].message.content
        
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": query})
        self.conversation_history.append({"role": "assistant", "content": advice})
        
        return {
            "advice": advice,
            "context_used": bool(context_prompt),
            "docs_referenced": len(self.uploaded_docs)
        } 