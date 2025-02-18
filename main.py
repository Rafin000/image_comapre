#main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
# from src.face_verification import verify_faces
import io
from celery.result import AsyncResult
from src.tasks import verify_faces_task, celery_app  

app = FastAPI(
    title="Face Verification API",
    description="An API to verify if two uploaded images belong to the same person.",
    version="1.0.0"
)

# @app.post('/verify_faces')
# async def verify_faces_api(
#     image1: UploadFile = File(...),
#     image2: UploadFile = File(...)
# ):
#     """Compares two images to determine if they belong to the same person."""
    
#     if not image1 or not image2:
#         raise HTTPException(status_code=400, detail="Both images are required")

#     # Read files into memory (BytesIO)
#     image1_data = io.BytesIO(await image1.read())
#     image2_data = io.BytesIO(await image2.read())

#     response = verify_faces(image1_data, image2_data)

#     return response


# task_results = {}

@app.post('/verify_faces_async')
async def verify_faces_async(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...)
):
    """Asynchronously compares two images to determine if they belong to the same person."""
    
    if not image1 or not image2:
        raise HTTPException(status_code=400, detail="Both images are required")

    # Read files into memory
    image1_bytes = await image1.read()
    image2_bytes = await image2.read()

    # Submit task to Celery
    task = verify_faces_task.delay(image1_bytes, image2_bytes)
    
    # Return task ID for client to check status
    return {"task_id": task.id, "status": "processing"}


@app.get('/task_result/{task_id}')
async def get_task_result(task_id: str):
    """Get the result of an asynchronous face verification task."""
    result = AsyncResult(task_id, app=celery_app)
    
    if result.ready():
        return {
            "task_id": task_id,
            "status": "completed",
            "result": result.result  
        }
    else:
        return {
            "task_id": task_id,
            "status": "processing"
        }
    

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)