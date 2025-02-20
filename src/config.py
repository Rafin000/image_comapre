import os

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY ", "43sae!@#wsf")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

    # Uvicorn
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 8000))
    RELOAD = os.getenv("RELOAD", "True").lower() == "true"
    WORKERS = int(os.getenv("WORKERS", 1))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    # DeepFace
    MODEL_NAME = os.getenv("MODEL_NAME", "Facenet512")
    DISTANCE_METRIC = os.getenv("DISTANCE_METRIC", "euclidean_l2")
    
