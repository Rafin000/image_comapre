#src/face_verification.py
# from deepface import DeepFace
# from fastapi import HTTPException
# import tempfile
# import io

# def verify_faces(image1_data: io.BytesIO, image2_data: io.BytesIO):
#     """Compare two face images using DeepFace with in-memory handling."""

#     try:
#         # Create temporary files in memory
#         with tempfile.NamedTemporaryFile(suffix=".jpg") as img1, tempfile.NamedTemporaryFile(suffix=".jpg") as img2:
#             img1.write(image1_data.getvalue())
#             img1.flush()
#             img2.write(image2_data.getvalue())
#             img2.flush()

#             result = DeepFace.verify(img1.name, img2.name, distance_metric='euclidean_l2', model_name='Facenet512')

#         distance = result['distance']
#         threshold = result['threshold']
#         similarity_percentage = (1 - (distance / threshold)) * 100

#         return {
#             "message": "Both images show the same person." if result["verified"] else "The images do not show the same person.",
#             "distance": distance,
#             "threshold": threshold,
#             "confidence": f"{similarity_percentage:.2f}%"
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error during face verification: {str(e)}")