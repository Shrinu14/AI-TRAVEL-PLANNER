# Use official slim Python image
FROM python:3.10-slim

# Set environment variables to reduce Python buffering and improve logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Kolkata

# Install system dependencies including Tini and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    tini \
    build-essential \
    curl \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Use Tini as the entrypoint for better signal handling
ENTRYPOINT ["/usr/bin/tini", "--"]

# Start FastAPI app using Uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "300"]
