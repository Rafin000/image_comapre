# --- Build Stage (Install dependencies) ---
    FROM python:3.10-slim AS builder

    # Set environment variables
    ENV PYTHONUNBUFFERED=1 \
        PYTHONDONTWRITEBYTECODE=1
    
    # Install system dependencies
    RUN apt-get update && apt-get install -y \
        libgl1-mesa-glx \
        libglib2.0-0 \
        curl \
        git && \
        apt-get clean && rm -rf /var/lib/apt/lists/*
    
    # Set working directory
    WORKDIR /app
    
    # Copy only the dependency files
    COPY requirements.txt ./
    
    # Install Python dependencies from requirements.txt
    RUN pip install --no-cache-dir -r requirements.txt
    
    # --- Final Stage (Minimal runtime) ---
    FROM python:3.10-slim
    
    # Set environment variables
    ENV PYTHONUNBUFFERED=1 \
        PYTHONDONTWRITEBYTECODE=1
    
    # Install system dependencies in the final stage
    RUN apt-get update && apt-get install -y \
        libgl1-mesa-glx \
        libglib2.0-0 && \
        apt-get clean && rm -rf /var/lib/apt/lists/*
    
    # Set working directory
    WORKDIR /app
    
    # Copy installed dependencies from the builder stage
    COPY --from=builder /usr/local /usr/local
    
    # Copy the source code from the src directory
    COPY ./src /app/src
    COPY main.py /app/main.py
    
    # Expose FastAPI port
    EXPOSE 8000
    
    # Run FastAPI application
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]