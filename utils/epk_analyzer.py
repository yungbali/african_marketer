from typing import Dict
import base64
from pathlib import Path
import fitz  # PyMuPDF for PDF handling
from PIL import Image
import io
from openai import OpenAI

class EPKAnalyzer:
    def __init__(self, openai_key: str):
        self.client = OpenAI(api_key=openai_key)
        
    def analyze_epk(self, epk_file, form_data: Dict) -> Dict:
        """Analyze EPK using Vision API"""
        try:
            # Convert PDF pages to images
            images = self._pdf_to_images(epk_file)
            
            # Analyze each page with Vision API
            analysis = []
            for img in images:
                encoded_image = self._encode_image(img)
                vision_analysis = self._analyze_with_vision(encoded_image, form_data)
                analysis.append(vision_analysis)
            
            # Combine analyses into marketing brief
            return self._generate_brief(analysis, form_data)
        except Exception as e:
            return {"error": str(e)}

    def _pdf_to_images(self, pdf_file) -> list:
        """Convert PDF pages to images"""
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        images = []
        
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x scale for better quality
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)
            
        return images

    def _encode_image(self, image: Image) -> str:
        """Convert PIL Image to base64"""
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def _analyze_with_vision(self, encoded_image: str, form_data: Dict) -> Dict:
        """Analyze image using OpenAI Vision API"""
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at analyzing Electronic Press Kits (EPKs) for musicians."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this EPK page and extract relevant marketing information."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        return {"content": response.choices[0].message.content}

    def _generate_brief(self, analyses: list, form_data: Dict) -> Dict:
        """Generate marketing brief from analyses"""
        combined_analysis = "\n".join([a["content"] for a in analyses])
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Generate a structured marketing brief based on EPK analysis."
                },
                {
                    "role": "user",
                    "content": f"EPK Analysis:\n{combined_analysis}\n\nForm Data:{form_data}"
                }
            ]
        )
        
        return {
            "brief": response.choices[0].message.content,
            "analyses": analyses
        }