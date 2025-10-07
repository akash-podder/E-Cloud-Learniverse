# Environment Variables Configuration

## Setup

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Update the values in `.env` for your environment

## Available Variables

### `VITE_BACKEND_API_BASE_URL`
- **Description**: Backend FastAPI API endpoint
- **Default**: `http://localhost:8002/api`
- **Examples**:
  - Local: `http://localhost:8002/api`
  - Docker: `http://fastapi-backend:8000/api`
  - Production: `https://api.yourdomain.com/api`

## Usage in Different Environments

### Local Development
```bash
# .env
VITE_BACKEND_API_BASE_URL=http://localhost:8002/api
```

### Docker Container
When building the Docker image, pass the environment variable:

**Option 1: Build-time (recommended for production)**
```dockerfile
# In Dockerfile
ARG VITE_BACKEND_API_BASE_URL=http://localhost:8000/api
ENV VITE_BACKEND_API_BASE_URL=$VITE_BACKEND_API_BASE_URL

# Build with custom value
docker build --build-arg VITE_BACKEND_API_BASE_URL=http://api.example.com/api -t react-app .
```

**Option 2: Runtime with env-cmd or similar**
```bash
# Install env-cmd
npm install env-cmd --save-dev

# Create different env files
# .env.docker
VITE_BACKEND_API_BASE_URL=http://fastapi-backend:8000/api

# Run with specific env
npm run build:docker
```

Update `package.json`:
```json
{
  "scripts": {
    "build:docker": "env-cmd -f .env.docker vite build"
  }
}
```

### Kubernetes Pod

**Option 1: Using ConfigMap**
```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: react-config
data:
  VITE_BACKEND_API_BASE_URL: "http://fastapi-web-app-service/api"
```

**Option 2: Using environment variables in Deployment**
```yaml
# deployment.yaml
spec:
  containers:
    - name: react-app
      image: react-app:latest
      env:
        - name: VITE_BACKEND_API_BASE_URL
          value: "http://fastapi-web-app-service/api"
```

**Option 3: Build-time with Helm values**
```yaml
# values.yaml
frontend:
  env:
    apiBaseUrl: "http://fastapi-web-app-service/api"

# In Dockerfile
ARG VITE_BACKEND_API_BASE_URL
ENV VITE_BACKEND_API_BASE_URL=$VITE_BACKEND_API_BASE_URL

# Build in CI/CD
docker build --build-arg VITE_BACKEND_API_BASE_URL={{ .Values.frontend.env.apiBaseUrl }} -t react-app .
```

## Important Notes

1. **Build-time vs Runtime**: Vite environment variables are embedded at **build time**, not runtime. If you need runtime configuration, consider:
   - Using a config.js file served separately
   - Using window.__ENV__ pattern
   - Rebuilding for different environments

2. **Security**: Never commit `.env` files with sensitive data. Always use `.env.example` as template.

3. **Prefix Required**: All Vite env variables must be prefixed with `VITE_` to be exposed to client-side code.

4. **Fallback**: The app has a fallback to `http://localhost:8000/api` if env variable is not set.

## Docker Example

### Dockerfile
```dockerfile
FROM node:18-alpine AS first_stage_react_app_builder

WORKDIR /app

# Accept build argument
ARG VITE_BACKEND_API_BASE_URL=http://localhost:8002/api
ENV VITE_BACKEND_API_BASE_URL=$VITE_BACKEND_API_BASE_URL

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=first_stage_react_app_builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Build and Run
```bash
# Build with custom API URL
docker build --build-arg VITE_BACKEND_API_BASE_URL=http://my-api:8000/api -t react-app .

# Run
docker run -p 3000:80 react-app
```

## Kubernetes Example

### Docker Build in CI/CD
```bash
# In your CI/CD pipeline
docker build \
  --build-arg VITE_BACKEND_API_BASE_URL=http://fastapi-web-app-service/api \
  -t your-registry/react-app:latest \
  .

docker push your-registry/react-app:latest
```

### Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: react-app
spec:
  replicas: 2
  template:
    spec:
      containers:
        - name: react-app
          image: your-registry/react-app:latest
          ports:
            - containerPort: 80
```

## Testing

Check if environment variable is loaded:
```javascript
console.log('API Base URL:', import.meta.env.VITE_BACKEND_API_BASE_URL);
```
