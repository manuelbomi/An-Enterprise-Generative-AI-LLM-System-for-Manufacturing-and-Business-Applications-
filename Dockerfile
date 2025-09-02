# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY app/ /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit and Prometheus ports
EXPOSE 8501 9001

# Use environment variables from .env (already mounted via docker-compose)
ENV PYTHONUNBUFFERED=1

# Command to run Streamlit
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
