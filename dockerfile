# 1. Base Image
FROM python:3.9-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy the dependencies file to the working directory
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirement.txt

# 5. Copy the rest of the application files to the container
COPY . .

# 6. Expose the Flask app port
EXPOSE 5000

# 7. Command to run the Flask app
CMD ["python", "run.py"]
