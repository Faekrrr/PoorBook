# Stage 1: Build the React app
FROM node:16 as build

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

# Stage 2: Serve the app with Nginx
FROM nginx:alpine

# Copy the Nginx configuration file
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Remove the default Nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy the build output to the Nginx static assets directory
COPY --from=build /app/build /usr/share/nginx/html

# Expose the port Nginx will run on
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
