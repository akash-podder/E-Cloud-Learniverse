# Kubernetes Service Discovery Implementation

## Problem Solved

**Original Issue:** Frontend running in browser cannot resolve Kubernetes service names like `fastapi-web-app-service` because:
- Browser runs on local machine, not inside Kubernetes cluster
- Kubernetes DNS only works for pod-to-pod communication
- Environment variables in Kubernetes deployment don't work because Vite embeds variables at build time

## Solution: Nginx Reverse Proxy

We've implemented an nginx reverse proxy inside the frontend container that:
1. **Accepts requests from the browser** at relative paths (`/api`)
2. **Proxies requests to the backend** using Kubernetes service discovery
3. **Returns responses to the browser** transparently

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Browser (localhost)                    │
│                                                             │
│  Makes request to: http://localhost:30005/api/messages     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Kubernetes Cluster (Kind)                      │
│                                                             │
│  ┌────────────────────────────────────────────┐            │
│  │  Frontend Pod (NodePort: 30005)            │            │
│  │                                             │            │
│  │  ┌─────────────────────────────────────┐   │            │
│  │  │  Nginx (listens on port 80)         │   │            │
│  │  │                                      │   │            │
│  │  │  location /api {                     │   │            │
│  │  │    proxy_pass http://fastapi...     │───┼──────┐     │
│  │  │  }                                   │   │      │     │
│  │  └─────────────────────────────────────┘   │      │     │
│  │                                             │      │     │
│  │  React Static Files (served by Nginx)      │      │     │
│  └────────────────────────────────────────────┘      │     │
│                                                       │     │
│                                                       ▼     │
│  ┌────────────────────────────────────────────┐            │
│  │  Backend Pod                                │            │
│  │                                             │            │
│  │  Service: fastapi-web-app-service:8083     │            │
│  │  FastAPI Application                        │            │
│  │                                             │            │
│  └────────────────────────────────────────────┘            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Details

### 1. Nginx Configuration (`nginx.conf`)

```nginx
location /api {
    proxy_pass http://fastapi-web-app-service:8083;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    # ... other headers
}
```

**Key Points:**
- Nginx runs **inside the pod**, so it can resolve Kubernetes service names
- `fastapi-web-app-service` is resolved via Kubernetes DNS
- Port `8083` is the internal cluster service port

### 2. Frontend Build Configuration

Build the React app with a **relative URL**:

```bash
docker build --build-arg VITE_BACKEND_API_BASE_URL=/api -t reactjs-frontend-e-cloud-docker-image:latest .
```

This tells the React app to make requests to `/api/*` (relative to current host).

### 3. Dockerfile Changes

```dockerfile
# Copy custom nginx configuration with reverse proxy for backend API
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

The nginx.conf is now copied into the container during build.

## Request Flow

1. **Browser → Frontend Pod**
   - User clicks button in React app
   - JavaScript makes request: `GET /api/messages`
   - Browser sends to: `http://localhost:30005/api/messages`

2. **Nginx Intercepts Request**
   - Nginx receives the request on port 80
   - Matches `location /api` rule
   - Prepares to proxy

3. **Nginx → Backend Service**
   - Nginx resolves `fastapi-web-app-service` via Kubernetes DNS
   - Forwards request to: `http://fastapi-web-app-service:8083/api/messages`
   - Backend processes request

4. **Backend → Nginx → Browser**
   - Backend returns JSON response
   - Nginx forwards response back to browser
   - React app receives data and updates UI

## Benefits

✅ **Browser doesn't need Kubernetes knowledge**
- Makes standard HTTP requests to relative URLs
- No CORS issues (same origin)

✅ **Service discovery handled by Kubernetes**
- Nginx resolves service names using cluster DNS
- Automatic load balancing across backend pods

✅ **Works in all environments**
- Local development (with port-forward)
- Kubernetes clusters (minikube, kind, cloud)
- Production deployments

✅ **Easy to maintain**
- Single nginx.conf file to configure
- No environment-specific frontend builds needed

## Testing

### Verify Nginx Configuration

```bash
# Access frontend pod
kubectl exec -it <frontend-pod-name> -- sh

# Check nginx config
cat /etc/nginx/conf.d/default.conf

# Test nginx configuration
nginx -t

# Check nginx logs
tail -f /var/log/nginx/access.log
```

### Verify Service Discovery

```bash
# From within frontend pod, test DNS resolution
kubectl exec -it <frontend-pod-name> -- nslookup fastapi-web-app-service

# Test connectivity
kubectl exec -it <frontend-pod-name> -- wget -O- http://fastapi-web-app-service:8083/api/messages
```

### Verify End-to-End

1. Port-forward frontend service:
   ```bash
   kubectl port-forward service/frontend-reactjs-service 3000:80
   ```

2. Open browser: `http://localhost:3000`

3. Open browser DevTools → Network tab

4. Click button to fetch messages

5. Verify request goes to `/api/messages` (relative URL)

## Comparison with Alternatives

| Approach | Pros | Cons |
|----------|------|------|
| **Nginx Reverse Proxy** ✅ | Simple, works everywhere, no CORS | Requires nginx config |
| Environment Variables | No extra config | Doesn't work (build-time only) |
| Direct Service Name | Simple | Only works inside cluster |
| Kubernetes Ingress | Production-ready | Complex setup, requires ingress controller |
| Service Mesh (Istio) | Advanced features | Overkill for simple apps |

## Common Issues & Solutions

### Issue: 502 Bad Gateway

**Cause:** Backend service name or port is wrong in nginx.conf

**Solution:**
```bash
# Verify service exists and port is correct
kubectl get svc fastapi-web-app-service
kubectl describe svc fastapi-web-app-service
```

### Issue: CORS Errors

**Cause:** CORS headers not properly configured

**Solution:** Our nginx.conf includes CORS headers. Verify:
```nginx
add_header 'Access-Control-Allow-Origin' '*' always;
```

### Issue: 404 Not Found on /api

**Cause:** Nginx config not loaded or path mismatch

**Solution:**
```bash
# Rebuild and reload image
docker build --build-arg VITE_BACKEND_API_BASE_URL=/api -t reactjs-frontend-e-cloud-docker-image:latest .
kind load docker-image reactjs-frontend-e-cloud-docker-image:latest --name mac-cluster-test
kubectl rollout restart deployment reactjs-frontend-deployment
```

## Files Modified

1. ✅ `nginx.conf` - Created with reverse proxy configuration
2. ✅ `Dockerfile` - Updated to copy nginx.conf
3. ✅ `DOCKER_BUILD.md` - Updated documentation
4. ℹ️ `kubernetes/frontend-react-app/*` - No changes needed (env vars removed)

## Next Steps

For production deployments, consider:
1. **Kubernetes Ingress** - For external access with proper domain names
2. **TLS/SSL** - Add HTTPS support
3. **Rate Limiting** - Protect backend from abuse
4. **Caching** - Cache static assets and API responses
5. **Monitoring** - Add prometheus metrics to nginx