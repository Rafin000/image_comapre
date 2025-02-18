# src/tasks.py
import tempfile
import io
from deepface import DeepFace
from celery import Celery

celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',  
    backend='redis://localhost:6379/0'
)

@celery_app.task
def verify_faces_task(image1_bytes, image2_bytes):
    """Compare two face images using DeepFace with Celery."""
    image1_data = io.BytesIO(image1_bytes)
    image2_data = io.BytesIO(image2_bytes)
    
    try:
        # Writing images to temporary files
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as img1, tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as img2:
            img1.write(image1_data.getvalue())
            img1.flush()  # Ensuring the data is fully written
            img2.write(image2_data.getvalue())
            img2.flush()

            # Perform face verification
            result = DeepFace.verify(img1.name, img2.name, distance_metric='euclidean_l2', model_name='Facenet512')

        # Extract distance and threshold from the result
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