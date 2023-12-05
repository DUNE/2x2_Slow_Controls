# Use an official Node runtime as a parent image
FROM node:alpine

# Set the working directory to /react-app
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package.json ./

# Install any needed packages specified in package.json
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Make port 3006 available to the world outside this container
EXPOSE 3006

# Run npm start when the container launches
CMD ["npm", "start", "--", "--host", "0.0.0.0", "--port", "3006"]