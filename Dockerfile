# Start from the oficial Python base image
FROM python:3.10

# Set the current working directory to /code.
# This is where we'll put the requirements.txt file.
WORKDIR /code

# Copy the file with the requirements to the /code directory.
# Copy only the file with the requirements first, not the rest of the code.
COPY ./requirements.txt /code/requirements.txt

# Install the package dependencies in the requirements file.
# Because the previous step copying the file could be detected by the Docker cache, this step will also use the Docker cache when available.
# Using the cache in this step will save you a lot of time when building the image again and again during development, instead of downloading and installing all the dependencies every time.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the python script inside the /code directory.
# As this has all the code which is what changes most frequently the Docker cache won't be used for this or any following steps easily.
COPY plot_transporter.py /code/plot_transporter.py
COPY plot_transporter.sh /code/plot_transporter.sh

# Make your script executable
RUN chmod +x plot_transporter.sh

# Define the command to run your script
CMD ["/code/plot_transporter.sh"]
