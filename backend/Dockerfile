# Use official Python runtime as base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt || true

# if a pyproject exists install editable package (allows `pip install -e .`)
COPY ../pyproject.toml ../pyproject.toml
RUN if [ -f ../pyproject.toml ]; then pip install -e ..; fi

# Copy rest of the application code
COPY . .

# Create upload directory for CSV files and ensure permissions
RUN mkdir -p uploads/csv && \
    chown -R root:root /app

# Expose port
EXPOSE 8000

# Add a non-root user for security
RUN useradd --create-home appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check (still runs as non-root user)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
