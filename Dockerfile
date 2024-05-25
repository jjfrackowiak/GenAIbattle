# Use an official Python runtime as a parent image
FROM python:3.11.7-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY backend.py .
COPY LIBS ./LIBS
COPY .env .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable to enable uvicorn's auto-reload
ENV UVICORN_CMD="uvicorn backend:app --host 0.0.0.0 --port 8000"

# Run uvicorn when the container launches
CMD ["sh", "-c", "$UVICORN_CMD"]
