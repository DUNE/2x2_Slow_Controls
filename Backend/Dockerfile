# DOCKER CONFIGURATION FILE
# Source: https://fastapi.tiangolo.com/deployment/docker/#build-a-docker-image-for-fastapi

# Start from the oficial Python base image
FROM python:3.10

# Set the current working directory to /code.
# This is where we'll put the requirements.txt file and the MyApp directory.
WORKDIR /code

# Copy the file with the requirements to the /code directory.
# Copy only the file with the requirements first, not the rest of the code.
# As this file doesn't change often, Docker will detect it and use the cache for this step, enabling the cache for the next step too.
COPY ./Backend/requirements.txt /code/requirements.txt

# Install the package dependencies in the requirements file.
# Because the previous step copying the file could be detected by the Docker cache, this step will also use the Docker cache when available.
# Using the cache in this step will save you a lot of time when building the image again and again during development, instead of downloading and installing all the dependencies every time.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# Getting the local server IP address
RUN export LOCAL_IP=$(bash -c 'hostname -I | cut -d" " -f1')

# Copy the ./app directory inside the /code directory.
# As this has all the code which is what changes most frequently the Docker cache won't be used for this or any following steps easily.
COPY ./Backend /code/app

# Set the command to run the uvicorn server.
# CMD takes a list of strings, each of these strings is what you would type in the command line separated by spaces.
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

