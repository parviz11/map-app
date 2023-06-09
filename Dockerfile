# Use the official Python base image
FROM python:3.11-slim

# Debug mode is False
ENV DASH_DEBUG_MODE False

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y nano

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port on which your application runs
EXPOSE 8050

# Set the entry point for the container
CMD ["gunicorn", "--workers=5", "--threads=1", "-b", "0.0.0.0:80", "app:server"]
