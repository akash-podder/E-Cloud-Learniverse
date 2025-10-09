# Multi-stage build for React frontend

# Stage 1: Build the React application
FROM node:22-alpine AS first_stage_react_app_builder

WORKDIR /app

# Define build argument to select environment file (defaults to "docker")
ARG ENV_FILE=docker

# Copy the selected environment file to .env
# ENV_FILE can be "docker" or "kubernetes"
COPY .env_${ENV_FILE} .env

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:alpine

# Copy built files from first_stage_react_app_builder stage
COPY --from=first_stage_react_app_builder /app/dist /usr/share/nginx/html

# Copy custom nginx configuration with reverse proxy for backend API
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80, because Nginx exposes port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
