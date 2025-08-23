import os
import sys
import hmac
import logging
import numpy as np
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from tasks import get_cheque_information
from celery_worker import celery_app

app = FastAPI(title="Cheque Information Extractor API", version="1.0.0", docs_url="/docs", redoc_url="/redoc", openapi_url="/openapi.json")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/api.log")
    ]
)

logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY_HEADER = APIKeyHeader(name="X-API-KEY")
API_KEY = os.getenv("API_KEY")

def verify_api_key(api_key: str = Depends(API_KEY_HEADER)):
    if not hmac.compare_digest(api_key, API_KEY):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key

@app.get("/health", tags=["Health Check"])
async def health_check(api_key: str = Depends(verify_api_key)):
    return {"status": "ok", "message": "Service is running"}

@app.post("/extract", tags=["Cheque Information Extraction"])
async def extract_cheque_info(
    file: UploadFile = File(...),
    api_key: str = Depends(verify_api_key)
) -> JSONResponse:
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image file.")
    
    try:
        file_content = await file.read()
        cheque_img = np.frombuffer(file_content, np.uint8)
        # task = get_cheque_information.delay(cheque_img)
        # result = task.get(timeout=30)
        # return JSONResponse(content={"status": "success", "data": result})
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error"
)