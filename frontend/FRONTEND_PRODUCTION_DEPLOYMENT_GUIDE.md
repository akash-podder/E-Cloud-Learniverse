# Frontend Production Deployment Guide

## Overview

This guide explains how React applications are built and served in production environments, specifically focusing on our Docker-based deployment with Nginx.

---

## Development vs Production

### Development Mode (`npm run dev`)
```bash
npm run dev
# - Vite dev server runs on port 5173
# - Hot Module Replacement (HMR) enabled
# - Source maps for debugging
# - Unminified code
# - Real-time reloading on file changes
```

### Production Mode (`npm run build`)
```bash
npm run build
# - Creates optimized static files (HTML, CSS, JS)
# - Code is minified and bundled
# - Tree-shaking removes unused code
# - Assets are hashed for cache busting
# - No dev server needed!
```

---

## What Happens During `npm run build`

When you run `npm run build`, Vite compiles your React application into **static files**:

```
/app/dist/
├── index.html                    # Single HTML entry point
├── assets/
│   ├── index-abc123.js          # Bundled JavaScript (minified)
│   ├── index-xyz789.css         # Bundled CSS (minified)
│   ├── logo-def456.png          # Optimized images
│   └── [other assets]
└── favicon.png                   # Static assets
```

### Key Transformations:

1. **JSX → JavaScript**: All React JSX is transpiled to vanilla JavaScript
2. **Bundling**: Multiple files are combined into optimized bundles
3. **Minification**: Code is compressed (whitespace removed, variables shortened)
4. **Tree Shaking**: Unused code is removed
5. **Code Splitting**: Large bundles are split for optimal loading
6. **Asset Optimization**: Images and other assets are optimized

**Important**: After build, React becomes **just static files** (HTML/CSS/JS). No Node.js runtime needed!

---

## Why Nginx for Production?

Since React (after build) is just static files, you need a **web server** to serve them. We use **Nginx** because:

### Advantages of Nginx:

✅ **Fast & Lightweight**: Minimal memory footprint
✅ **Battle-tested**: Used by millions of production websites
✅ **Efficient Static File Serving**: Optimized for serving HTML/CSS/JS
✅ **Built-in Caching**: Reduces server load
✅ **Gzip Compression**: Reduces bandwidth usage
✅ **Load Balancing**: Can distribute traffic across multiple servers
✅ **Reverse Proxy**: Can proxy API requests to backend
✅ **SSL/TLS Support**: Easy HTTPS setup

### Nginx's Role:

```
User Request (http://localhost:3000)
         ↓
    Nginx (Port 80)
         ↓
Serves /usr/share/nginx/html/index.html
         ↓
Browser loads JS/CSS assets
         ↓
React app runs in browser
         ↓
API calls go to FastAPI backend
```

---

## Docker Multi-Stage Build Explained

Our Dockerfile uses a **multi-stage build** to optimize the final image size:

### Stage 1: Builder (Node.js)

```dockerfile
FROM node:18-alpine AS first_stage_react_app_builder

WORKDIR /app

# Accept build argument for API URL
ARG VITE_BACKEND_API_BASE_URL=http://localhost:8000/api
ENV VITE_BACKEND_API_BASE_URL=$VITE_BACKEND_API_BASE_URL

# Install dependencies
COPY package*.json ./
RUN npm ci

# Build the application
COPY . .
RUN npm run build
# Output: /app/dist/ (static files)
```

**Purpose**: Compile React app to static files
**Size**: ~500MB (includes Node.js, npm, build tools)
**Discarded**: Yes, after build completes

### Stage 2: Production (Nginx)

```dockerfile
FROM nginx:alpine

# Copy built files from first_stage_react_app_builder stage
COPY --from=first_stage_react_app_builder /app/dist /usr/share/nginx/html

# Expose port 80 (Nginx's default port)
EXPOSE 80

# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
```

**Purpose**: Serve static files
**Size**: ~25MB (just Nginx + static files)
**Runs**: This is the final production container

### Why Multi-Stage?

- **Smaller Image**: Final image is 20x smaller (25MB vs 500MB)
- **Faster Deployment**: Less data to transfer
- **More Secure**: No build tools or source code in production
- **Cleaner**: Only production dependencies

---

## Understanding `CMD ["nginx", "-g", "daemon off;"]`

This command starts Nginx in the container:

### Breakdown:

- **`nginx`**: Starts the Nginx web server
- **`-g "daemon off;"`**: Runs Nginx in **foreground mode**

### Why `daemon off;`?

**Problem**: By default, Nginx runs as a background daemon (detaches from terminal)

**Issue with Docker**:
- Docker containers need a **foreground process**
- If the main process exits, container stops
- If Nginx runs as daemon, it backgrounds itself → container exits immediately

**Solution**: `daemon off;` keeps Nginx in foreground → container stays running

```bash
# Without "daemon off;"
nginx          # Starts, backgrounds itself, returns
# Container exits immediately ❌

# With "daemon off;"
nginx -g "daemon off;"   # Starts and stays in foreground
# Container keeps running ✅
```

---

## Complete Production Flow Diagram

```
┌───────────────────────────────────────────────────┐
│  Stage 1: first_stage_react_app_builder (Node.js)│
│                                                   │
│  npm ci          → Install dependencies           │
│  npm run build   → Compile React                  │
│                  → Optimize & Bundle              │
│                                                   │
│  Output: /app/dist/                               │
│    ├── index.html                                 │
│    ├── assets/index-abc123.js                     │
│    ├── assets/index-xyz789.css                    │
│    └── favicon.png                                │
│                                                   │
│  (Stage 1 container is discarded)                 │
└───────────────────────────────────────────────────┘
                  ↓
┌───────────────────────────────────────────────────┐
│  Stage 2: Production (Nginx)                      │
│                                                   │
│  COPY /app/dist → /usr/share/nginx/html           │
│  CMD nginx -g "daemon off;"                       │
│                                                   │
│  Nginx serves static files on port 80            │
└───────────────────────────────────────────────────┘
                  ↓
        Docker Port Mapping
        (3000:80 in docker-compose.yml)
                  ↓
          User's Browser
      http://localhost:3000
                  ↓
    Browser receives index.html
                  ↓
    Loads bundled JS/CSS from /assets/
                  ↓
    React app runs in browser
                  ↓
    Makes API calls to FastAPI
    http://localhost:8002/api
```

---

## How React Works in Production

### Client-Side Rendering (CSR)

React is a **client-side framework** - all logic runs in the user's browser:

1. **Server sends**: `index.html` + bundled `JavaScript`
2. **Browser downloads**: JS/CSS assets
3. **Browser executes**: React JavaScript code
4. **React renders**: DOM elements in browser
5. **User interacts**: React handles updates in browser
6. **API calls**: React fetches data from FastAPI backend

### Why No Node.js Needed in Production?

```
Development:
  Node.js → Vite Dev Server → Hot Reload → Browser

Production:
  Nginx → Static Files → Browser
  (No Node.js needed!)
```

The **entire React application** is compiled into JavaScript that runs in the browser. The server (Nginx) only needs to send files - it doesn't execute any React code.

---

## Port Configuration

### In the Container:

```dockerfile
EXPOSE 80  # Nginx's default port
```

Nginx always listens on **port 80 inside the container**.

### In Docker Compose:

```yaml
ports:
  - "3000:80"  # localhost:3000 → container:80
```

**Port mapping**:
- **Host (your machine)**: Port 3000
- **Container (Nginx)**: Port 80

**Access**: `http://localhost:3000` → routed to → `container port 80` → Nginx serves files

### Why Port 80?

Port 80 is:
- **HTTP standard port**: Default for web traffic
- **Nginx default**: Nginx is configured to listen on 80
- **Convention**: Most web servers use 80 (HTTP) or 443 (HTTPS)

---

## Alternative Production Servers

While we use Nginx, you could also serve React with:

### 1. Apache HTTP Server
```dockerfile
FROM httpd:alpine
COPY --from=first_stage_react_app_builder /app/dist /usr/local/apache2/htdocs/
```

### 2. Caddy
```dockerfile
FROM caddy:alpine
COPY --from=first_stage_react_app_builder /app/dist /usr/share/caddy
```

### 3. Node.js (serve)
```dockerfile
FROM node:18-alpine
COPY --from=first_stage_react_app_builder /app/dist /app
RUN npm install -g serve
CMD ["serve", "-s", "/app", "-l", "3000"]
```

### 4. Python HTTP Server
```dockerfile
FROM python:3.9-alpine
COPY --from=first_stage_react_app_builder /app/dist /app
WORKDIR /app
CMD ["python", "-m", "http.server", "8000"]
```

### Why We Choose Nginx:

| Server | Pros | Cons |
|--------|------|------|
| **Nginx** ✅ | Fast, lightweight, production-ready | Requires configuration |
| Apache | Feature-rich, well-documented | Heavier than Nginx |
| Caddy | Auto HTTPS, simple config | Less mature ecosystem |
| Node serve | Simple, familiar | Not optimized for production |
| Python | Built-in, easy | Slow, not for production |

**Nginx is the industry standard** for serving static files in production.

---

## Environment Variables in Production

### Build-Time Variables

Environment variables are **embedded at build time**:

```dockerfile
ARG VITE_BACKEND_API_BASE_URL=http://localhost:8000/api
ENV VITE_BACKEND_API_BASE_URL=$VITE_BACKEND_API_BASE_URL
```

**Important**: Once built, the API URL is **hardcoded** in the JavaScript bundle.

### Changing API URL:

**Option 1: Rebuild with different URL**
```bash
docker build \
  --build-arg VITE_BACKEND_API_BASE_URL=http://production-api.com/api \
  -t react-app .
```

**Option 2: Multiple builds for different environments**
```bash
# Development build
docker build --build-arg VITE_BACKEND_API_BASE_URL=http://localhost:8002/api -t react-app:dev .

# Production build
docker build --build-arg VITE_BACKEND_API_BASE_URL=https://api.myapp.com/api -t react-app:prod .
```

**Option 3: Runtime configuration (advanced)**
- Use `window.__ENV__` pattern
- Serve config.js separately
- Fetch config from endpoint

---

## Deployment Checklist

### Before Deployment:

- [ ] Set correct `VITE_BACKEND_API_BASE_URL` for your environment
- [ ] Test build locally: `npm run build && npm run preview`
- [ ] Check environment variables are set correctly
- [ ] Verify API endpoints are accessible from production
- [ ] Update CORS settings in FastAPI backend

### Build Commands:

```bash
# Local build test
cd frontend/e-cloud-learniverse-frontend-react
npm run build
npm run preview  # Preview production build locally

# Docker build
docker build \
  --build-arg VITE_BACKEND_API_BASE_URL=http://your-api-url/api \
  -t react-frontend:latest \
  .

# Docker Compose
docker-compose up --build react_frontend
```

### Verify Deployment:

```bash
# Check container is running
docker ps | grep react

# Check logs
docker logs react_learniverse_container

# Test health check
curl http://localhost:3000

# Check API connection (in browser console)
fetch('http://localhost:8002/api/messages')
```

---

## Troubleshooting

### Issue: White Screen / Blank Page

**Cause**: Assets not loading correctly

**Solution**:
1. Check browser console for errors
2. Verify base URL in `vite.config.js`
3. Check nginx is serving files: `docker exec react_learniverse_container ls /usr/share/nginx/html`

### Issue: API Calls Failing

**Cause**: Incorrect API URL or CORS issues

**Solution**:
1. Check `VITE_BACKEND_API_BASE_URL` in build
2. Verify CORS settings in FastAPI backend
3. Check network in browser DevTools

### Issue: Container Exits Immediately

**Cause**: Nginx running as daemon

**Solution**: Ensure `CMD ["nginx", "-g", "daemon off;"]` in Dockerfile

### Issue: Large Image Size

**Cause**: Not using multi-stage build

**Solution**:
- Use multi-stage build (builder + nginx)
- Add `.dockerignore` to exclude node_modules
- Clean up unnecessary files

---

## Performance Optimization

### 1. Gzip Compression (Nginx)

Create `nginx.conf`:
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
gzip_min_length 1000;
```

### 2. Caching Headers

```nginx
location /assets/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 3. Code Splitting

Vite automatically code-splits. Verify in `vite.config.js`:
```javascript
build: {
  rollupOptions: {
    output: {
      manualChunks: {
        vendor: ['react', 'react-dom']
      }
    }
  }
}
```

---

## Security Best Practices

1. **Run as non-root user**:
```dockerfile
RUN addgroup -g 101 -S nginx && adduser -S -D -H -u 101 -h /var/cache/nginx -s /sbin/nologin -G nginx nginx
USER nginx
```

2. **Remove unnecessary packages**:
```dockerfile
RUN apk del --purge build-dependencies
```

3. **Use specific image versions**:
```dockerfile
FROM nginx:1.25-alpine  # Not "latest"
```

4. **Scan for vulnerabilities**:
```bash
docker scan react-frontend:latest
```

---

## Summary

### Key Concepts:

1. **React in production = Static files** (HTML, CSS, JS)
2. **No Node.js needed** - just a web server (Nginx)
3. **Multi-stage build** - Small, optimized images
4. **Nginx serves files** - Fast, efficient, production-ready
5. **`daemon off;`** - Keeps container running
6. **Environment variables** - Embedded at build time

### Production Flow:

```
npm run build → Static files → Docker build → Nginx container → Production
```

### Access Points:

- **Development**: http://localhost:5173 (Vite dev server)
- **Production (Docker)**: http://localhost:3000 (Nginx)
- **Backend API**: http://localhost:8002/api

---

## Additional Resources

- [Vite Build Documentation](https://vitejs.dev/guide/build.html)
- [Nginx Docker Image](https://hub.docker.com/_/nginx)
- [React Production Build](https://react.dev/learn/start-a-new-react-project#production-grade-react-frameworks)
- [Docker Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)

---

**Last Updated**: 2025-10-07
