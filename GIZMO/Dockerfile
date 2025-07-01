# DOCKER CONFIGURATION FILE
# Source: https://fastapi.tiangolo.com/deployment/docker/#build-a-docker-image-for-fastapi

# Start from the oficial Python base image
FROM python:3.10

# Set the current working directory to /code.
# This is where we'll put the requirements.txt file.
WORKDIR /app

# Copy the file with the requirements to the /code directory.
# Copy only the file with the requirements first, not the rest of the code.
# As this file doesn't change often, Docker will detect it and use the cache for this step, enabling the cache for the next step too.
COPY requirements.txt /app/requirements.txt

# Install the package dependencies in the requirements file.
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the ./app directory inside the /code directory.
COPY ./Source /app/Source
COPY ./Source/GIZMO_run.py /app/Source/GIZMO_run.py
COPY ./CONFIG /app/CONFIG

# Make your script executable
RUN chmod +x Source/GIZMO_run.sh

# Define the command to run your script
CMD ["/app/Source/GIZMO_run.sh"]


