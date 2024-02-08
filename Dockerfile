# Set arguments
ARG BASE_CONTAINER=python:3.8

# Set the base image. 
FROM --platform=linux/amd64 $BASE_CONTAINER

# Make a directory for our app
WORKDIR /producer

# Install dependencies
COPY requirements.txt .
COPY app.py .

RUN pip install -r requirements.txt
RUN pip install 'flask[async]'

# Copy source code
COPY ./api ./api

# Run the application
CMD ["python", "-m", "api"]