# Docker Setup Instructions

## Prerequisites

Before testing the Docker setup, ensure you have the following installed:
1. Docker Engine
2. Docker Compose

## Testing the Docker Setup

1. Build the Docker images:
   ```bash
   docker-compose build
   ```

2. Run the application:
   ```bash
   docker-compose up
   ```

3. Access the application:
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. To stop the application:
   ```bash
   docker-compose down
   ```

## Troubleshooting

If you encounter issues:

1. Check that all required files are present:
   - `models/YOLOfinetuned.pt` (the YOLO model file)
   - All source code in `src/` directory
   - Frontend files in `src/web/frontend/` (index.html, script.js, styles.css)

2. Ensure sufficient system resources:
   - The application uses machine learning models which can be memory intensive
   - Allocate at least 4GB RAM to Docker

3. Check logs if services fail to start:
   ```bash
   docker-compose logs <service_name>
   ```

4. Rebuild images if you make changes to the code:
   ```bash
   docker-compose up --build
   ```

## Architecture Notes

The Docker setup now uses a single base image for all Python services:
- The backend API service runs Gunicorn with the FastAPI application
- The Celery worker service uses the same image but with a different command
- The frontend service uses the same image but runs the Python HTTP server

This approach reduces image size and simplifies maintenance while maintaining clear service separation.

## System Dependencies

The Docker image includes several system libraries required for OpenCV and other dependencies:
- `libgl1`, `libglib2.0-0`, `libsm6`, `libxext6`, `libxrender-dev`: Required for OpenCV
- `libgomp1`: OpenMP library for parallel processing
- `libgtk-3-0`: GUI toolkit (sometimes needed by OpenCV)

If you encounter errors related to missing system libraries (like `libGL.so.1`), ensure these dependencies are included in the Dockerfile.