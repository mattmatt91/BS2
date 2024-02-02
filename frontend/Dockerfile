# Use Node.js as a base image
FROM node:16-slim

# Set the working directory in the container
WORKDIR /usr/src/app/


# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install
# --only=production

# Copy the production build directory and other necessary files
COPY . ./

# Command to run the application
CMD ["npm", "start"]
