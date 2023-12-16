# Use an official Python runtime as a parent image
FROM python:3.9-slim
# Set environment variables

# Set work directory
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . ./

# Run the application
CMD ["uvicorn", "main:app", "--host", "192.168.1.30", "--port", "6000", "--reload"]
