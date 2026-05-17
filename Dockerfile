# Use an official lightweight Python runtime as a parent image
FROM python:3.11-slim

# Set system environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_MAX_UPLOAD_SIZE=10

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (needed for git, SQLite, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code into the container
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Health check to ensure Streamlit container is responsive
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the Streamlit web dashboard
ENTRYPOINT ["streamlit", "run", "app.py"]
