import os
import json
import shutil
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn
from pydantic import BaseModel

from utils.document_processor import process_document
from utils.openai_analyzer import analyze_claim

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create necessary directories
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("templates", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("results", exist_ok=True)

app = FastAPI(title="Insurance Fraud Detector")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

class AnalysisResult(BaseModel):
    summary: str
    trustworthiness_score: int
    detailed_analysis: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze/", response_model=AnalysisResult)
async def analyze_document(file: UploadFile = File(...)):
    try:
        # Check file extension
        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in ["pdf", "txt"]:
            raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")
        
        logger.info(f"Processing file: {file.filename} of type {file_extension}")
        
        # Save the uploaded file
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"File saved to {file_path}")
        
        # Process the document
        try:
            text = process_document(file_path, file_extension)
            logger.info("Document processed successfully")
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
        
        # Analyze the document
        try:
            analysis_result = analyze_claim(text)
            logger.info("Document analyzed successfully")
        except Exception as e:
            logger.error(f"Error analyzing document: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error analyzing document: {str(e)}")
        
        # Save the result
        result_path = f"results/{file.filename.split('.')[0]}_analysis.json"
        try:
            with open(result_path, "w") as f:
                json.dump(analysis_result, f, indent=4)
            logger.info(f"Results saved to {result_path}")
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
            # Continue even if saving fails
        
        return AnalysisResult(**analysis_result)
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
    finally:
        # Clean up the uploaded file
        if 'file_path' in locals() and os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Temporary file {file_path} removed")
            except Exception as e:
                logger.error(f"Error removing temporary file: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
