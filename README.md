# Cheque Information Extractor

This application extracts various components from a cheque, namely signature, receiver, account, and amount using YOLO object detection. It also provides OCR functionality for account number recognition.

## Features

- Object detection for cheque components using YOLO
- OCR for account number recognition
- FastAPI backend with Celery for asynchronous processing
- Docker support for easy deployment

## Setup

1. Install dependencies:
   ```bash
   pip install -e .
   ```

2. Or install from requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Method 1: Manual Start (Development)

You need to start each service separately:

1. Start Redis server:
   ```bash
   redis-server
   ```

2. Start Celery worker:
   ```bash
   celery -A src.web.backend.celery_worker worker --loglevel=info
   ```

3. Start the FastAPI application:
   ```bash
   gunicorn src.web.backend.api:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --log-level info
   ```

4. Start the frontend server:
   ```bash
   python main.py
   ```

### Method 2: Using Docker Compose (Recommended for Production)

```bash
docker-compose up
```

This will start all services:
- Redis database
- FastAPI backend on port 8000
- Celery worker for task processing
- Frontend server on port 8080

Access the application at:
- Frontend: http://localhost:8080
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Method 3: Using the Startup Script

```bash
./start_all.sh
```

## API Usage

Once the backend is running, you can access:

- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Cheque Extraction: http://localhost:8000/extract

The `/extract` endpoint accepts:
- `file`: The cheque image file (PNG, JPG, JPEG, TIFF, BMP, GIF)
- `perform_ocr`: Boolean flag to enable OCR on account number
- `X-API-KEY`: Header with your API key (default: f64bdf6ae22c46efa50b0a98c322ded4)

## Environment Variables

- `API_KEY`: Required API key for authentication
- `CELERY_BROKER_URL`: Redis URL for Celery (default: redis://localhost:6379/0)
- `CELERY_RESULT_BACKEND`: Redis URL for Celery results (default: redis://localhost:6379/1)