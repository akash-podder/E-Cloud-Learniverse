# Use Python 3.9 slim image for smaller size
FROM python:3.9-slim

# Set working directory in container
WORKDIR /web_app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt /web_app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /web_app/

COPY . /web_app/
COPY .env_docker /web_app/.env

# Expose port
EXPOSE 9998

# Health check
# The health check monitors the container's application status. Docker periodically runs curl -f http://localhost:9998/index to verify the FastAPI app is responding. If it fails 3 times, Docker marks the container as "unhealthy", which helps orchestration tools (like Docker Compose, Kubernetes) automatically restart or replace failing containers.
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:9998/health-check || exit 1

# Start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9998"]