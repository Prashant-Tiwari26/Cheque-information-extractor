import os
import sys
import logging
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from celery_worker import celery_app
from models.detection.detect import detect_components

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/tasks.log")
    ]
)

logger = logging.getLogger(__name__)

@celery_app.task
def get_cheque_information(cheque_img: np.array) -> dict:
    ...