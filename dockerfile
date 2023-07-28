# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code to the container
COPY . /app

# Install git
RUN apt-get update && apt-get install -y git

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the entrypoint command to run the Flask application
CMD ["python", "app.py"]
