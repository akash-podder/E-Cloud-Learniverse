# Docker Compose Commands

## Project Architecture

The application consists of 3 services:
1. **react_frontend** - React app served with Nginx (Port 3000)
2. **fastapi_web_app** - FastAPI backend (Port 8002)
3. **learniverse_db** - PostgreSQL database (Port 5434)

---

## Quick Start

### Build and Start All Services
```bash
docker-compose up --build
```

### Start in Background (Detached Mode)
```bash
docker-compose up -d --build
```

---

## Individual Service Commands

### Build Specific Service
```bash
# Build frontend only
docker-compose build react_frontend

# Build backend only
docker-compose build fastapi_web_app
```

### Start Specific Service
```bash
# Start frontend only (and its dependencies)
docker-compose up react_frontend

# Start backend only (and its dependencies)
docker-compose up fastapi_web_app
```

---

## Service Management

### View Running Containers
```bash
docker-compose ps
```

### View Logs
```bash
# All services
docker-compose logs

# Follow logs (real-time)
docker-compose logs -f

# Specific service logs
docker-compose logs react_frontend
docker-compose logs fastapi_web_app
docker-compose logs learniverse_db

# Last 50 lines
docker-compose logs --tail=50 -f
```

### Stop Services
```bash
# Stop all services (containers still exist)
docker-compose stop

# Stop specific service
docker-compose stop react_frontend
```

### Start Stopped Services
```bash
docker-compose start
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart fastapi_web_app
```

---

## Cleanup Commands

### Stop and Remove Containers
```bash
docker-compose down
```

### Remove Containers, Networks, and Volumes
```bash
docker-compose down -v
```

### Remove Everything Including Images
```bash
docker-compose down --rmi all -v
```

---

## Development Workflow

### Rebuild After Code Changes

**Frontend Changes:**
```bash
# Rebuild and restart frontend
docker-compose up -d --build react_frontend
```

**Backend Changes:**
```bash
# Backend has hot-reload enabled, no rebuild needed
# If you need to rebuild:
docker-compose up -d --build fastapi_web_app
```

### Access Services

- **React Frontend**: http://localhost:3000
- **FastAPI Backend**: http://localhost:8002
- **FastAPI Docs**: http://localhost:8002/docs
- **PostgreSQL**: localhost:5434

---

## Execute Commands Inside Containers

### Access Container Shell
```bash
# Frontend (Nginx container)
docker-compose exec react_frontend sh

# Backend
docker-compose exec fastapi_web_app sh

# Database
docker-compose exec learniverse_db bash
```

### Run Commands in Container
```bash
# Check FastAPI version
docker-compose exec fastapi_web_app python -c "import fastapi; print(fastapi.__version__)"

# Access PostgreSQL
docker-compose exec learniverse_db psql -U postgres -d e_cloud_learniverse_db

# List database tables
docker-compose exec learniverse_db psql -U postgres -d e_cloud_learniverse_db -c "\dt"
```

---

## Database Commands

### Connect to PostgreSQL
```bash
docker-compose exec learniverse_db psql -U postgres -d e_cloud_learniverse_db
```

### Database Backup
```bash
docker-compose exec learniverse_db pg_dump -U postgres e_cloud_learniverse_db > backup.sql
```

### Database Restore
```bash
docker-compose exec -T learniverse_db psql -U postgres -d e_cloud_learniverse_db < backup.sql
```

### Reset Database
```bash
# Stop and remove volumes
docker-compose down -v

# Start fresh
docker-compose up -d
```

---

## Health Checks

### Check Service Health
```bash
# View health status
docker-compose ps

# Check specific service health
docker inspect react_learniverse_container --format='{{.State.Health.Status}}'
docker inspect fastapi_learniverse_container --format='{{.State.Health.Status}}'
docker inspect postgres_learniverse_db_container --format='{{.State.Health.Status}}'
```

---

## Troubleshooting

### View Service Details
```bash
docker-compose config
```

### Check Port Conflicts
```bash
# Check if ports are in use
lsof -i :3000  # Frontend
lsof -i :8002  # Backend
lsof -i :5434  # Database
```

### Remove Orphan Containers
```bash
docker-compose down --remove-orphans
```

### Force Rebuild (No Cache)
```bash
docker-compose build --no-cache
docker-compose up -d
```

### Network Issues
```bash
# Inspect network
docker network inspect e-cloud-fastapi-learniverse_fastapi_network

# Restart network
docker-compose down
docker-compose up -d
```

---

## Production Deployment

### Build for Production
```bash
# Build with production environment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```

### Scale Services
```bash
# Scale backend to 3 instances
docker-compose up -d --scale fastapi_web_app=3
```

---

## Environment Variables

### Override API URL for Frontend
```bash
# Build with custom API URL
docker-compose build --build-arg VITE_BACKEND_API_BASE_URL=http://api.production.com/api react_frontend
```

### Set Environment Variables
```bash
# Create .env file in project root
DATABASE_USER=postgres
DATABASE_PASSWORD=secretpassword
POSTGRES_DB=mydb

# Docker Compose will automatically use these
docker-compose up -d
```

---

## Common Workflows

### Full Rebuild
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
docker-compose logs -f
```

### Development Workflow
```bash
# Start all services
docker-compose up -d

# Watch logs
docker-compose logs -f

# Make changes to code...

# Rebuild frontend after changes
docker-compose up -d --build react_frontend

# Backend auto-reloads (no rebuild needed)
```

### Stop and Clean Everything
```bash
docker-compose down -v --rmi all
docker system prune -a --volumes
```

---

## Docker Compose File Structure

```yaml
services:
  react_frontend:    # Port 3000 -> 80
  fastapi_web_app:   # Port 8002 -> 9998
  learniverse_db:    # Port 5434 -> 5432

networks:
  fastapi_network    # Bridge network for all services

volumes:
  postgres_data      # Persistent PostgreSQL data
```

---

## Tips

1. **Hot Reload**: Backend has `--reload` flag, so code changes are reflected immediately
2. **Frontend Changes**: Require rebuild since it's a static build with Nginx
3. **Database Data**: Persisted in named volume `postgres_data`
4. **Logs**: Use `-f` flag to follow logs in real-time
5. **Port Conflicts**: Make sure ports 3000, 8002, 5434 are free
