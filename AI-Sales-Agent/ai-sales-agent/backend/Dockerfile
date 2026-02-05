# -----------------------------
# Base image
# -----------------------------
FROM python:3.10-slim

# -----------------------------
# Environment variables
# -----------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# -----------------------------
# System dependencies
# -----------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Working directory
# -----------------------------
WORKDIR /app

# -----------------------------
# Copy requirements first (cache-friendly)
# -----------------------------
COPY backend/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Copy application code
# -----------------------------
COPY backend /app/backend
COPY docs /app/docs

# -----------------------------
# Create vectorstore directory
# -----------------------------
RUN mkdir -p /app/vectorstore

# -----------------------------
# Expose API port
# -----------------------------
EXPOSE 8002

# -----------------------------
# Run FastAPI server
# -----------------------------
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8002"]
