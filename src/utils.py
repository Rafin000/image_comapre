from pathlib import Path

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_DIR = Path('temp')
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def allowed_file(filename: str) -> bool:
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_filename(filename: str) -> str:
    """Sanitize filename to prevent security issues."""
    return filename.replace(" ", "_").replace("..", "").lower()
