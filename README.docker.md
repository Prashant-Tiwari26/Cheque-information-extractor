# Docker Setup for Cheque Information Extractor

This project includes Docker configuration for easy deployment and development.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. Build and start all services:
   ```bash
   docker-compose up --build
   ```

2. Access the application:
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

3. To stop all services:
   ```bash
   docker-compose down
   ```

## Services Overview

- **redis**: Redis database for Celery task queue
- **backend**: FastAPI backend service (runs on port 8000)
- **worker**: Celery worker for processing tasks (uses same image as backend)
- **frontend**: Simple HTTP server for frontend files (runs on port 8080)

## Environment Variables

The following environment variables are used:

- `API_KEY`: Authentication key for API access
- `CELERY_BROKER_URL`: Redis URL for Celery broker
- `CELERY_RESULT_BACKEND`: Redis URL for Celery results

These are set in the `docker-compose.yml` file.

## Volumes

- `redis_data`: Persistent storage for Redis data
- `./logs`: Log files from all services
- `./models`: Model files (YOLOfinetuned.pt)

## Development

To rebuild and restart a specific service:
```bash
docker-compose up --build --force-recreate <service_name>
```

To view logs for a specific service:
```bash
docker-compose logs <service_name>
```

## Health Checks

Each service includes health checks:
- Backend: http://localhost:8000/health

## Architecture

The Docker setup uses a single base image (`Dockerfile`) for all Python services:
- The **backend** service runs the FastAPI application using Gunicorn
- The **worker** service runs the Celery worker with a custom command
- The **frontend** service serves static files using Python's built-in HTTP server

This approach reduces image size and simplifies maintenance while maintaining clear service separation.

## System Dependencies

The Docker image includes several system libraries required for OpenCV and other dependencies:
- `libgl1`, `libglib2.0-0`, `libsm6`, `libxext6`, `libxrender-dev`: Required for OpenCV
- `libgomp1`: OpenMP library for parallel processing
- `libgtk-3-0`: GUI toolkit (sometimes needed by OpenCV)

These dependencies ensure that all machine learning libraries work correctly in the containerized environment.

## Model Handling

The application uses pre-trained models:
1. YOLO model (`YOLOfinetuned.pt`) - Should be present in the `models/` directory
2. TrOCR model for OCR - Downloaded during Docker image build

The Docker build process automatically downloads the required TrOCR model from Hugging Face, so the application will have full OCR functionality when deployed with Docker.