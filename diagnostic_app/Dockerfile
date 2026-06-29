# Use the official Python image from DockerHub
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Copy the model file into the container (ensure it's inside the Docker build context)
COPY model.joblib /app/model.joblib

# Install system dependencies and Python dependencies
RUN apt-get update && \
    apt-get install -y build-essential gcc libatlas-base-dev && \
    pip install --no-cache-dir -r requirements.txt

# Expose the port that the Flask app will run on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
