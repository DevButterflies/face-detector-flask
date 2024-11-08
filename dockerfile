# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

#System Dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirement.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirement.txt

# Copy the current directory contents into the container
COPY . /app

# Install the required Python packages
RUN pip install --no-cache-dir -r requirement.txt

# Expose the port the app runs on
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=run.py

# Run the command to start the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
