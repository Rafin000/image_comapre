from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
from src.face_verification import verify_faces
from src.utils import UPLOAD_DIR, allowed_file, secure_filename

app = FastAPI(
    title="Face Verification API",
    description="An API to verify if two uploaded images belong to the same person.",
    version="1.0.0"
)

@app.post('/verify_faces', summary="Verify Face Similarity", tags=["Face Verification"])
async def verify_faces_api(
    image1: UploadFile = File(..., description="First image file (jpg, jpeg, png)"),
    image2: UploadFile = File(..., description="Second image file (jpg, jpeg, png)")
):
    """
    Compares two images to determine if they belong to the same person.

    **Request:**
    - `image1`: The first image file (jpg, jpeg, png)
    - `image2`: The second image file (jpg, jpeg, png)

    **Response:**
    - A JSON object containing verification results.
    """
    if not image1 or not image2:
        raise HTTPException(status_code=400, detail="Both images are required")

    if not allowed_file(image1.filename) or not allowed_file(image2.filename):
        raise HTTPException(status_code=400, detail="Invalid file type. Only png, jpg, jpeg are allowed.")

    # Secure filenames and set file paths
    image1_path = UPLOAD_DIR / secure_filename(image1.filename)
    image2_path = UPLOAD_DIR / secure_filename(image2.filename)

    # Save uploaded images
    with image1.file as f1, image2.file as f2:
        with open(image1_path, 'wb') as img1, open(image2_path, 'wb') as img2:
            img1.write(f1.read())
            img2.write(f2.read())

    # Perform face verification
    response = verify_faces(str(image1_path), str(image2_path))

    # Cleanup uploaded images after processing
    image1_path.unlink(missing_ok=True)
    image2_path.unlink(missing_ok=True)

    return response

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)