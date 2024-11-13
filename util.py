
from fastapi import HTTPException
from PyPDF2 import PdfReader
from typing import Dict, List
import fitz

class Util:
    def extractPDFText(self, file_path: str) -> str:
        try:
            reader = PdfReader(file_path)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading PDF file: {str(e)}")
    
    def extractTextFileContent(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading text file: {str(e)}")
    def cleanText(self, text: str) -> str:
        cleanedText = text.replace('\n', ' ').replace('\\', ' ')
        cleanedText = ' '.join(cleanedText.split())

        return cleanedText
    
    def maskWordsInPDF(self, file_path: str, keywords_dict: Dict[str, List[str]]):
        try:
            doc = fitz.open(file_path)
            for page in doc:
                for key, words in keywords_dict.items():
                    for word in words:
                        text_instances = page.search_for(word)
                        for inst in text_instances:
                            page.add_redact_annot(inst, fill=(0, 0, 0), cross_out=True)

                page.apply_redactions()
            
            doc.saveIncr() 
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error modifying PDF file: {str(e)}")
        
    def maskWordsInText(self, text: str, keywords_dict: Dict[str, List[str]]) -> str:
        for key, words in keywords_dict.items():
            for word in words:
                replacement_text = f"[{key} REDACTED]"
                text = text.replace(word, replacement_text)
        
        return text