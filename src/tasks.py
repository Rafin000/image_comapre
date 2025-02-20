# src/tasks.py
import tempfile
import io
from deepface import DeepFace
from celery import Celery
from src.config import BaseConfig

celery_app = Celery(
    'tasks',
    broker=BaseConfig.CELERY_BROKER_URL,
    backend=BaseConfig.CELERY_RESULT_BACKEND
)

@celery_app.task
def verify_faces_task(image1_bytes, image2_bytes):
    """Compare two face images using DeepFace with Celery."""
    image1_data = io.BytesIO(image1_bytes)
    image2_data = io.BytesIO(image2_bytes)
    
    try:
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as img1, \
             tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as img2:
            img1.write(image1_data.getvalue())
            img1.flush()
            img2.write(image2_data.getvalue())
            img2.flush()

            # Use configuration for DeepFace
            result = DeepFace.verify(
                img1.name, 
                img2.name, 
                distance_metric=BaseConfig.DISTANCE_METRIC,
                model_name=BaseConfig.MODEL_NAME
            )

        distance = result['distance']
        threshold = result['threshold']
        similarity_percentage = (1 - (distance / threshold)) * 100

        return {
            "message": "Both images show the same person." if result["verified"] else "The images do not show the same person.",
            "distance": distance,
            "threshold": threshold,
            "confidence": f"{similarity_percentage:.2f}%"
        }

    except Exception as e:
        return {"error": f"Error during face verification: {str(e)}"}