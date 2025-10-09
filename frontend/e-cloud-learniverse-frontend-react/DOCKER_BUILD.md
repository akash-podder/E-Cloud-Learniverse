# Docker Build Instructions for React Frontend

## Overview
The Dockerfile supports both default configuration (using `.env_docker`) and custom build-time configuration via build arguments.

**NEW: Nginx Reverse Proxy for Kubernetes Service Discovery**
- The frontend now includes an nginx reverse proxy configuration
- Nginx proxies `/api` requests to the backend service using Kubernetes service discovery
- This allows the frontend to work seamlessly in Kubernetes clusters

## Build Options

### 1. Default Build for Docker Compose (Uses `.env_docker`)
This is the default behavior - uses values from `.env_docker` file:

```bash
sudo docker build -f frontend/e-cloud-learniverse-frontend-react/Dockerfile -t reactjs-frontend-e-cloud-docker-image:latest ./frontend/e-cloud-learniverse-frontend-react
```

**Configuration from `.env_docker`:**
- `VITE_BACKEND_API_BASE_URL=http://localhost:8002/api`

**Use case:** Local development with Docker Compose

---

### 2. Build for Kubernetes (Uses `.env_kubernetes`)
Build with Kubernetes configuration using `.env_kubernetes` file:

```bash
sudo docker build -f frontend/e-cloud-learniverse-frontend-react/Dockerfile --build-arg ENV_FILE=kubernetes -t reactjs-frontend-e-cloud-docker-image:kubernetes ./frontend/e-cloud-learniverse-frontend-react
```

**Configuration from `.env_kubernetes`:**
- `VITE_BACKEND_API_BASE_URL=/api`

**Use case:** Kubernetes deployments (Kind, Minikube, EKS, GKE, AKS)

---

### 3. Custom Environment Files

You can create additional environment files for different environments:

**Create `.env_staging`:**
```bash
VITE_BACKEND_API_BASE_URL=https://api-staging.example.com/api
```

**Build with custom environment:**
```bash
sudo docker build -f frontend/e-cloud-learniverse-frontend-react/Dockerfile --build-arg ENV_FILE=staging -t reactjs-frontend-e-cloud-docker-image:staging ./frontend/e-cloud-learniverse-frontend-react
```

**Create `.env_production`:**
```bash
VITE_BACKEND_API_BASE_URL=https://api.example.com/api
```

**Build for production:**
```bash
sudo docker build -f frontend/e-cloud-learniverse-frontend-react/Dockerfile --build-arg ENV_FILE=production -t reactjs-frontend-e-cloud-docker-image:prod ./frontend/e-cloud-learniverse-frontend-react
```

---

## How It Works

1. **ARG Declaration**: The Dockerfile defines `ENV_FILE` as a build argument (defaults to "docker")
2. **Environment File Selection**: The build process copies `.env_${ENV_FILE}` to `.env`
   - Default: `.env_docker` (for local Docker Compose)
   - Kubernetes: `.env_kubernetes` (for K8s deployments)
   - Custom: `.env_staging`, `.env_production`, etc.
3. **Build Time Injection**: Vite embeds the environment variables into the JavaScript bundle during build
4. **Nginx Proxy**: The nginx reverse proxy handles routing to backend services

---

## Important Notes

⚠️ **Vite Environment Variables are Build-Time, Not Runtime**
- `VITE_*` variables are embedded into the JavaScript bundle at build time
- Changing environment variables in Kubernetes pod specs will NOT affect the frontend
- You must rebuild the Docker image with different build args for different environments

---

## Testing the Build

After building, you can verify the environment variable by inspecting the built files:

```bash
# Run the container
docker run -d -p 3000:80 --name test-frontend reactjs-frontend-e-cloud-docker-image:kubernetes

# Check the built JavaScript files for the API URL
docker exec test-frontend grep -r "fastapi-web-app-service" /usr/share/nginx/html/

# Clean up
docker stop test-frontend && docker rm test-frontend
```

---

## Kubernetes Deployment Workflow (RECOMMENDED)

Using the `.env_kubernetes` file with nginx reverse proxy for seamless Kubernetes service discovery:

1. **Build image for Kubernetes:**
   ```bash
   sudo docker build -f frontend/e-cloud-learniverse-frontend-react/Dockerfile --build-arg ENV_FILE=kubernetes -t reactjs-frontend-e-cloud-docker-image:kubernetes ./frontend/e-cloud-learniverse-frontend-react
   ```

2. **Load image into Kind cluster:**
   ```bash
   kind load docker-image reactjs-frontend-e-cloud-docker-image:kubernetes --name mac-cluster-test
   ```

3. **Apply deployment:**
   ```bash
   kubectl apply -f kubernetes/frontend-react-app/reactjs-frontend-app-deployment.yml
   ```

4. **Verify deployment:**
   ```bash
   kubectl get pods
   kubectl logs -l real-madrid-app=reactjs-frontend-e-cloud-learniverse-pod
   ```

**How it works:**
- `.env_kubernetes` sets `VITE_BACKEND_API_BASE_URL=/api`
- Browser makes request to `/api/messages` (relative URL)
- Nginx (running in the pod) intercepts the request
- Nginx proxies to `http://fastapi-web-app-service:8083/api/messages` using Kubernetes service discovery
- Response returns to browser through nginx

---

## Build Arguments Reference

| Argument | Description | Default | Options |
|----------|-------------|---------|---------|
| `ENV_FILE` | Environment file to use | `docker` | `docker`, `kubernetes`, `staging`, `production`, or custom |

---

## Nginx Reverse Proxy Configuration

The `../nginx/nginx.conf` file is configured to:
- Serve React static files from `/usr/share/nginx/html`
- Proxy all `/api/*` requests to `http://fastapi-web-app-service:8083`
- Add CORS headers for cross-origin requests
- Enable gzip compression for better performance
- Provide health check endpoint at `/health`

To modify the backend service name or port, edit the `/frontend/nginx/nginx.conf` file:
```nginx
proxy_pass http://fastapi-web-app-service:8083;
```

---

## Troubleshooting

**Problem**: Frontend still points to wrong API URL after deployment

**Solution**:
- Ensure you rebuilt the Docker image with the correct build argument
- Load the new image into your Kubernetes cluster
- Restart the pods: `kubectl rollout restart deployment reactjs-frontend-deployment`
- Clear browser cache and hard refresh

**Problem**: Kubernetes service discovery not working

**Solution**:
- Use **Option A** (nginx reverse proxy with relative URL `/api`)
- This ensures nginx (inside the pod) handles service discovery
- Browser only needs to know about relative paths, not Kubernetes service names

**Problem**: CORS errors when accessing API

**Solution**:
- The nginx.conf includes CORS headers by default
- Verify the backend service name and port in nginx.conf match your deployment

**Problem**: Want to add more build-time configuration

**Solution**:
1. Add the variable to `.env_docker` as default
2. Add `ARG VARIABLE_NAME` in Dockerfile (line 9)
3. Update the RUN command to include the new variable in the conditional override