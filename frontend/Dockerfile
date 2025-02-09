# Use Node.js image for React
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy the React app code
COPY . .

# Expose the frontend port
EXPOSE 8080

# CMD [ "npm", "run", "dev" ]
CMD [ "npm", "run", "dev" ]