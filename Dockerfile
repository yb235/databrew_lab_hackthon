FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY pyproject.toml pytest.ini ./

# Create directory for SQLite database
RUN mkdir -p /app/data

# Set environment variables
ENV HOST=0.0.0.0 \
    PORT=3001 \
    DATABASE_URL=sqlite:////app/data/emotion_interpretation.db \
    PYTHONUNBUFFERED=1

# Expose port
EXPOSE 3001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:3001/health').raise_for_status()" || exit 1

# Run application
CMD ["python", "src/main.py"]
