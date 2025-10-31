# Node.js LTS with Alpine for small image size
FROM node:20-alpine

# Install bash for startup script
RUN apk add --no-cache bash

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Set environment to development
ENV ELEVENTY_ENV=development

# Build the site
RUN npm run build

# Start the development server
CMD ["npm", "start"]
