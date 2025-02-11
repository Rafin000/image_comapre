from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path

from src.face_verification import verify_faces
from src.utils import UPLOAD_DIR, allowed_file, secure_filename


app = FastAPI()

@app.post('/verify')
async def verify_faces_api(image1: UploadFile = File(...), image2: UploadFile = File(...)):
    """API endpoint to verify if two images belong to the same person."""
    if not image1 or not image2:
        raise HTTPException(status_code=400, detail="Both images are required")

    if not allowed_file(image1.filename) or not allowed_file(image2.filename):
        raise HTTPException(status_code=400, detail="Invalid file type. Only png, jpg, jpeg are allowed.")

    image1_path = UPLOAD_DIR / secure_filename(image1.filename)
    image2_path = UPLOAD_DIR / secure_filename(image2.filename)

    with image1.file as f1, image2.file as f2:
        with open(image1_path, 'wb') as img1, open(image2_path, 'wb') as img2:
            img1.write(f1.read())
            img2.write(f2.read())

    response = verify_faces(str(image1_path), str(image2_path))

    # Cleanup uploaded images
    image1_path.unlink(missing_ok=True)
    image2_path.unlink(missing_ok=True)

    return response

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
