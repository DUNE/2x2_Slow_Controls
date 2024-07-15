# Start from the oficial Python base image
FROM python:3.10

# Set the current working directory to /code.
# This is where we'll put the requirements.txt file.
WORKDIR /code

# Copy the file with the requirements to the /code directory.
# Copy only the file with the requirements first, not the rest of the code.
COPY ./SPELLMAN/requirements.txt /code/requirements.txt

# Install the package dependencies in the requirements file.
# Because the previous step copying the file could be detected by the Docker cache, this step will also use the Docker cache when available.
# Using the cache in this step will save you a lot of time when building the image again and again during development, instead of downloading and installing all the dependencies every time.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the /SPELLMAN directory inside the /code directory.
# As this has all the code which is what changes most frequently the Docker cache won't be used for this or any following steps easily.
COPY ./SPELLMAN /code/SPELLMAN

# Make your script executable
RUN chmod +x SPELLMAN/SendSpellManHVToDB.sh
COPY SPELLMAN/monitor_spellman.py /code/monitor_spellman.py
COPY SPELLMAN/config.ini /code/config.ini

# Define the command to run your script
CMD ["/code/SPELLMAN/SendSpellManHVToDB.sh"]

