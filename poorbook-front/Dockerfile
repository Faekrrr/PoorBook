# Use an official node image as the base image
FROM node:16

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app
RUN npm run build

# Install serve to serve the build folder
RUN npm install -g serve

# Set the command to serve the React app
CMD ["serve", "-s", "build"]

# Expose the port the app runs on
EXPOSE 5000
