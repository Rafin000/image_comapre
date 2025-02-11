from deepface import DeepFace
from fastapi import HTTPException

def verify_faces(image1_path: str, image2_path: str):
    """Compare two face images using DeepFace."""
    try:
        result = DeepFace.verify(image1_path, image2_path, distance_metric='euclidean_l2')

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
        raise HTTPException(status_code=500, detail=f"Error during face verification: {str(e)}")
