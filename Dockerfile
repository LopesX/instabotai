# Create a file called secret.txt with 
# yourusername:password
# And save it then run 
# docker build .
# Docker run [IMAGE]
# Use an official Python runtime as a parent image
FROM python:3.7.2

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Run Cmake

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y cmake

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 800

# Define environment variable
ENV NAME World

# Run app.py when the container launches
ENTRYPOINT ["python3", "example.py"]
