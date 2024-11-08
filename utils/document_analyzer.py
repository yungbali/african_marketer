import fitz  # PyMuPDF
import pandas as pd
from datetime import datetime

class DocumentAnalyzer:
    def __init__(self):
        self.uploaded_docs = set()
        
    def process_document(self, file, filename):
        try:
            # Extract content using Python tools
            extracted_data = self._extract_all_content(file, filename)
            
            # Generate a basic analysis report without OpenAI
            analysis_report = self._generate_basic_report(extracted_data)
            
            return {
                "status": "success",
                "raw_content": extracted_data,
                "analysis": analysis_report,
                "message": "Content extracted successfully"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing document: {str(e)}"
            }

    def _extract_all_content(self, file, filename):
        extracted_data = {
            "text_content": [],
            "metadata": {},
            "tables": [],
            "images": [],
            "statistics": {
                "word_count": 0,
                "page_count": 0,
                "image_count": 0,
                "table_count": 0
            }
        }
        
        if filename.lower().endswith('.pdf'):
            pdf_content = file.read()
            doc = fitz.open(stream=pdf_content, filetype="pdf")
            
            # Get metadata
            extracted_data["metadata"] = {
                "title": doc.metadata.get("title", ""),
                "author": doc.metadata.get("author", ""),
                "subject": doc.metadata.get("subject", ""),
                "keywords": doc.metadata.get("keywords", ""),
                "page_count": len(doc)
            }
            
            extracted_data["statistics"]["page_count"] = len(doc)
            
            # Process each page
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Extract text
                text = page.get_text()
                if text.strip():
                    extracted_data["text_content"].append({
                        "page": page_num + 1,
                        "content": text
                    })
                    extracted_data["statistics"]["word_count"] += len(text.split())
                
                # Extract images - Fixed version
                for img_index, img in enumerate(page.get_images()):
                    try:
                        xref = img[0]  # xref number
                        image_info = {
                            "page": page_num + 1,
                            "image_index": img_index,
                            "width": img[2],
                            "height": img[3],
                            "colorspace": img[5],
                            "size_bytes": img[7] if len(img) > 7 else None
                        }
                        extracted_data["images"].append(image_info)
                        extracted_data["statistics"]["image_count"] += 1
                    except Exception as e:
                        print(f"Error extracting image: {str(e)}")
                
                # Extract tables
                tables = page.get_tables()
                if tables:
                    extracted_data["tables"].append({
                        "page": page_num + 1,
                        "tables": tables
                    })
                    extracted_data["statistics"]["table_count"] += 1
        
        return extracted_data 