# Start from the oficial Python base image
FROM python:3.10

# Set the current working directory to /code.
# This is where we'll put the requirements.txt file.
WORKDIR /code

# Copy the python script inside the /code directory.
# As this has all the code which is what changes most frequently the Docker cache won't be used for this or any following steps easily.
COPY log_reader.py /code/log_reader.py
COPY log_reader.sh /code/log_reader.sh

# Make your script executable
RUN chmod +x log_reader.sh

# Define the command to run your script
CMD ["/code/log_reader.sh"]