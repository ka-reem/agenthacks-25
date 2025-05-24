# Use an official Python runtime as a parent image
FROM python:3.10.4

# Set the working directory in the container
WORKDIR /app

# Copy only the server folder into the container at /app/server
COPY server /app/server

# Copy requirements.txt separately
COPY requirements.txt /app/

# Install GCC and other necessary build tools before installing Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    libasound2-dev \
    git

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

