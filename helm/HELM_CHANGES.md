# Helm Chart Changes Summary

## Changes Made to Align with Kubernetes Directory

This document summarizes the changes made to the Helm chart to match the updated Kubernetes configurations.

---

## 1. Backend FastAPI Service Changes

### Changed: Service Port
**File:** `helm/helm-e-cloud-learniverse/values.yaml`

```yaml
# OLD
service:
  port: 80

# NEW
service:
  port: 8083  # Changed for internal cluster communication
```

**Reason:** The backend service port was updated from 80 to 8083 to match the nginx reverse proxy configuration in the frontend.

---

## 2. Frontend ReactJS Deployment Changes

### Changed: Image Tag
**File:** `helm/helm-e-cloud-learniverse/values.yaml`

```yaml
# OLD
image:
  tag: latest

# NEW
image:
  tag: kubernetes  # Use :kubernetes tag for K8s builds
```

**Reason:** The frontend now uses a separate Docker image built specifically for Kubernetes with nginx reverse proxy configuration.

### Removed: Environment Variables
**Files:**
- `helm/helm-e-cloud-learniverse/values.yaml`
- `helm/helm-e-cloud-learniverse/templates/frontend-reactjs-deployment.yml`

```yaml
# COMMENTED OUT (no longer needed)
# env:
#   backendApiUrl: "http://fastapi-web-app-service:8083/api"
```

**Reason:** Vite environment variables (VITE_*) are embedded at build time, not runtime. The frontend image is now built with `VITE_BACKEND_API_BASE_URL=/api`, and nginx handles the reverse proxy to the backend service.

---

## 3. Nginx Reverse Proxy Architecture

### How It Works Now:

```
Browser (localhost:30005)
    ↓
Frontend Pod (nginx + React static files)
    ↓ /api/* requests
Nginx Reverse Proxy (inside frontend pod)
    ↓ proxies to
Backend Service (fastapi-web-app-service:8083)
```

### Key Points:

1. **Frontend Build**: Must be built with `--build-arg ENV_FILE=kubernetes`
2. **Nginx Configuration**: Located at `frontend/e-cloud-learniverse-frontend-react/nginx/nginx.conf`
3. **Service Discovery**: Nginx (running inside the pod) can resolve Kubernetes service names
4. **CORS**: Backend CORS settings updated to allow requests from nginx proxy

---

## 4. Updated Values Reference

### Backend (FastAPI)
```yaml
fastapi:
  service:
    port: 8083          # Internal cluster port
    targetPort: 9998    # Container port
    nodePort: 30004     # External access port
```

### Frontend (ReactJS)
```yaml
frontend:
  image:
    tag: kubernetes     # Must use kubernetes build
  service:
    port: 3000
    targetPort: 80      # Nginx listens on port 80
    nodePort: 30005
```

---

## 5. Build and Deploy Workflow

### Step 1: Build Frontend Image for Kubernetes
```bash
sudo docker build -f frontend/e-cloud-learniverse-frontend-react/Dockerfile \
  --build-arg ENV_FILE=kubernetes \
  -t reactjs-frontend-e-cloud-docker-image:kubernetes \
  ./frontend/e-cloud-learniverse-frontend-react
```

### Step 2: Load Images into Kind
```bash
kind load docker-image e-cloud-fastapi-docker-image:latest --name mac-cluster-test
kind load docker-image reactjs-frontend-e-cloud-docker-image:kubernetes --name mac-cluster-test
kind load docker-image postgres:17 --name mac-cluster-test
```

### Step 3: Install or Upgrade Helm Chart
```bash
# Install
helm install e-cloud helm/helm-e-cloud-learniverse

# Upgrade
helm upgrade e-cloud helm/helm-e-cloud-learniverse

# Uninstall
helm uninstall e-cloud
```

### Step 4: Verify Deployment
```bash
helm status e-cloud
kubectl get all
kubectl get pods
kubectl get svc
```

---

## 6. Environment-Specific Deployments

### Development Environment
```bash
# Use values-dev.yml with custom settings
helm install e-cloud-dev helm/helm-e-cloud-learniverse \
  -f helm/helm-e-cloud-learniverse/values-dev.yml
```

### Staging Environment
```bash
helm install e-cloud-staging helm/helm-e-cloud-learniverse \
  -f helm/helm-e-cloud-learniverse/values-staging.yml
```

### Production Environment
```bash
helm install e-cloud-prod helm/helm-e-cloud-learniverse \
  -f helm/helm-e-cloud-learniverse/values-prod.yml
```

---

## 7. Testing the Deployment

### Port Forward Services
```bash
# Backend
kubectl port-forward service/fastapi-web-app-service 8002:8083

# Frontend
kubectl port-forward service/reactjs-frontend-app-service 3000:80
```

### Access Applications
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8002/api
- **API Docs**: http://localhost:8002/docs

### Check Logs
```bash
# Backend
kubectl logs -l ramos-app-name=fastapi-web-app-e-cloud-pod

# Frontend
kubectl logs -l real-madrid-app=reactjs-frontend-e-cloud-learniverse-pod

# Database
kubectl logs -l app=postgres-e-cloud-pod
```

---

## 8. Troubleshooting

### Frontend Not Connecting to Backend

**Problem**: Frontend makes requests to wrong URL

**Solution**:
1. Verify frontend image is built with `ENV_FILE=kubernetes`
2. Check nginx.conf proxies to correct backend service:
   ```nginx
   proxy_pass http://fastapi-web-app-service:8083;
   ```
3. Restart frontend pods:
   ```bash
   kubectl rollout restart deployment reactjs-frontend-deployment
   ```

### Service Discovery Not Working

**Problem**: Nginx cannot resolve backend service name

**Solution**:
1. Verify backend service exists:
   ```bash
   kubectl get svc fastapi-web-app-service
   ```
2. Check service port is 8083:
   ```bash
   kubectl describe svc fastapi-web-app-service
   ```
3. Test DNS resolution from frontend pod:
   ```bash
   kubectl exec -it <frontend-pod> -- nslookup fastapi-web-app-service
   ```

### CORS Errors

**Problem**: Browser shows CORS errors

**Solution**:
1. Check backend CORS settings in `backend/main.py`
2. Verify nginx.conf includes CORS headers
3. Backend should allow `allow_credentials=False` with wildcard origins

---

## 9. Files Modified

### Helm Chart Files
- ✅ `helm/helm-e-cloud-learniverse/values.yaml`
  - Updated backend service port: 80 → 8083
  - Updated frontend image tag: latest → kubernetes
  - Commented out frontend env variables

- ✅ `helm/helm-e-cloud-learniverse/templates/frontend-reactjs-deployment.yml`
  - Commented out environment variable section
  - Added explanatory comments

- ✅ `helm/helm-e-cloud-learniverse/templates/backend-fastapi-service.yml`
  - No changes needed (already templated correctly)

### Supporting Files
- ✅ `frontend/e-cloud-learniverse-frontend-react/nginx/nginx.conf`
  - Nginx reverse proxy configuration
  - Proxies /api to backend service

- ✅ `frontend/e-cloud-learniverse-frontend-react/.env_kubernetes`
  - Sets `VITE_BACKEND_API_BASE_URL=/api`

- ✅ `backend/main.py`
  - Updated CORS to support nginx proxy

---

## 10. Next Steps

1. **Test Helm Installation**:
   ```bash
   helm lint helm/helm-e-cloud-learniverse
   helm install e-cloud helm/helm-e-cloud-learniverse --dry-run --debug
   ```

2. **Deploy to Cluster**:
   ```bash
   helm install e-cloud helm/helm-e-cloud-learniverse
   ```

3. **Verify Everything Works**:
   - Check all pods are running
   - Test frontend can reach backend
   - Verify data persistence in PostgreSQL

4. **Create Environment-Specific Values**:
   - `values-dev.yml`
   - `values-staging.yml`
   - `values-prod.yml`

---

## Summary

The Helm chart has been updated to support the new nginx reverse proxy architecture for Kubernetes service discovery. The main changes are:

1. Backend service port changed to 8083
2. Frontend uses `:kubernetes` tagged image
3. Environment variables removed from frontend (handled at build time)
4. Nginx reverse proxy enables seamless service-to-service communication

All changes maintain backwards compatibility and can be easily reverted if needed.
