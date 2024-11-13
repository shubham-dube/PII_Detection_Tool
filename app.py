from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import mimetypes
import tempfile
import os
import json
from extract_text import PIIExtractor
from util import Util

app = FastAPI()
    
@app.post('/api/v1/getSensitiveData')
async def getSensitiveData(file: UploadFile = File(...)):
    util = Util()
    piiObject = PIIExtractor()
    fileType, _ = mimetypes.guess_type(file.filename)

    with tempfile.NamedTemporaryFile(delete=False) as tempFile:
        tempFile.write(await file.read())
        tempFilePath = tempFile.name
    
    if fileType == 'application/pdf':
        fileText = util.extractPDFText(tempFilePath)
    elif 'text' in fileType:
        fileText = util.extractTextFileContent(tempFilePath)
    else:
        os.remove(tempFilePath) 
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {fileType}")
    
    os.remove(tempFilePath) 
    sensitiveData = piiObject.getAllSensitiveData(util.cleanText(fileText))
    return sensitiveData

@app.post('/api/v1/redactSensitiveData')
async def redactSensitiveData(replacements: str, file: UploadFile = File(...) ):
    util = Util()
    try:
        replacementsObj = json.loads(replacements)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format for replacements")
    
    name, fileExt = os.path.splitext(file.filename)
    fileType, _ = mimetypes.guess_type(file.filename)

    with tempfile.NamedTemporaryFile(delete=False) as tempFile:
        tempFile.write(await file.read())
        tempFilePath = tempFile.name
    
    if fileType == 'application/pdf':
        util.maskWordsInPDF(tempFilePath, replacementsObj)
        return FileResponse(tempFilePath, media_type=fileType, filename=os.path.basename(f"{name}_REDACTED"))

    elif 'text' in fileType:
        fileText = util.extractTextFileContent(tempFilePath)
        redactedText =util.maskWordsInText(util.cleanText(fileText), replacementsObj)

        output_file_path = tempfile.mktemp(suffix=fileExt)

        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(redactedText)

        os.remove(tempFilePath) 
        return FileResponse(output_file_path, media_type=fileType, filename=os.path.basename(f"{name}_REDACTED"))

    else:
        os.remove(tempFilePath) 
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {fileType}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
