from fastapi import FastAPI, UploadFile, File, HTTPException
import mimetypes
from PyPDF2 import PdfReader
import tempfile
import os
from extract_text import PIIExtractor

app = FastAPI()

def extractPDFText(file_path: str) -> str:
    try:
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF file: {str(e)}")

def extractTextFileContent(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading text file: {str(e)}")
    
def cleanText(text: str) -> str:
    cleanedText = text.replace('\n', ' ').replace('\\', ' ')
    cleanedText = ' '.join(cleanedText.split())

    return cleanedText

@app.post('/api/v1/getSensitiveData')
async def getSensitiveData(file: UploadFile = File(...)):
    fileType, _ = mimetypes.guess_type(file.filename)

    with tempfile.NamedTemporaryFile(delete=False) as tempFile:
        tempFile.write(await file.read())
        tempFilePath = tempFile.name
    
    fileText = ""
    
    if fileType == 'application/pdf':
        fileText = extractPDFText(tempFilePath)

    
    elif 'text' in fileType:
        fileText = extractTextFileContent(tempFilePath)
    
    else:
        os.remove(tempFilePath) 
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {fileType}")

    os.remove(tempFilePath)

    piiObject = PIIExtractor()

    object = piiObject.find_pii_in_text(cleanText(fileText))
    print(object)

    return object

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
