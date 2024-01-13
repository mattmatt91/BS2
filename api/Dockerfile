# Use an official Python runtime as a base image
FROM python:3.9-slim

# Install system dependencies required by OpenCV
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app/

RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libi2c-dev \
    python3-dev


RUN pip install --no-cache-dir rpi.gpio

ENV READTHEDOCS=True
RUN pip install --upgrade pip setuptools wheel

# RUN pip3 install picamera2

# Copy the requirements file into the container
COPY ./requirements.txt ./

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . ./


# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
