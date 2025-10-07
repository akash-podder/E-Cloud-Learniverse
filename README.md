# E-Cloud-Learniverse

## Project Overview

#### To Clone the Repository
```bash
git clone https://github.com/akash-podder/E-Cloud-Learniverse.git
```

**E-Cloud-Learniverse** is a comprehensive end-to-end web application that demonstrates modern cloud-native development practices and container orchestration. This project showcases the complete journey from development to deployment using industry-standard tools and technologies.

### Key Features & Achievements

- **End-to-End Web Application**: Developed a complete web application with FastAPI backend and PostgreSQL database
- **Containerization**: Containerized with Docker for consistent deployments and scalability
- **Kubernetes Orchestration**: Deployed on Kubernetes using Helm charts, demonstrating expertise in container orchestration
- **Cloud-Native DevOps**: Implements modern DevOps practices with cloud-native technologies

### Technologies Used

- **Backend**: FastAPI (Python web framework)
- **Database**: PostgreSQL 17
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Kubernetes
- **Package Management**: Helm Charts
- **Local Development**: Kind (Kubernetes in Docker)

---

## Quick Start

### Prerequisites

- Python 3.8+
- Docker & Docker Compose
- Kubernetes (kubectl)
- Helm 3.x
- Kind (for local Kubernetes cluster)

### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/akash-podder/E-Cloud-FastAPI-Learniverse.git
   cd E-Cloud-FastAPI-Learniverse
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv my_venv
   source my_venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run in Development Mode**
   ```bash
   fastapi dev main.py
   ```

4. **Run with Uvicorn (Production)**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --reload
   ```

---

## Docker Commands

### Basic Docker Setup

```bash
# Create Docker network
sudo docker network create fastapi-network

# Run PostgreSQL container
sudo docker run -d --name my-postgres-container-fastapi \
  --network fastapi-network \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=e_cloud_learniverse_db \
  postgres:17

# Build application image
sudo docker build --tag e-cloud-fastapi-docker-image .

# Run application container
sudo docker run --rm --name my-fastapi-web-container \
  --network fastapi-network \
  --publish 8002:9998 \
  -v $(pwd)/.env_docker:/web_app/.env \
  e-cloud-fastapi-docker-image
```

### Docker Compose

```bash
# Build and run with Docker Compose
sudo docker-compose up --build

# Run in background
sudo docker-compose up -d
```

---

## Kubernetes Commands

### Kind Cluster Setup

```bash
# Install Kind and kubectl
brew install kind kubectl

# Create Kind cluster
kind create cluster --name mac-cluster-test --image kindest/node:v1.30.6

# Load Docker image to Kind cluster
kind load docker-image e-cloud-fastapi-docker-image:latest --name mac-cluster-test
```

### Deploy with Kubernetes Manifests

```bash
# Apply PostgreSQL resources
kubectl apply -f kubernetes/postgres/postgres-deployment.yml
kubectl apply -f kubernetes/postgres/postgres-service.yml

# Apply FastAPI application resources
kubectl apply -f kubernetes/fastapi-web-app/fastapi-web-app-deployment.yml
kubectl apply -f kubernetes/fastapi-web-app/fastapi-web-app-service.yml

# Port forward to access application
kubectl port-forward service/fastapi-web-app-service 8002:80
```

### Clean up Kubernetes Resources

```bash
kubectl delete -f kubernetes/postgres/postgres-deployment.yml
kubectl delete -f kubernetes/postgres/postgres-service.yml
kubectl delete -f kubernetes/fastapi-web-app/fastapi-web-app-deployment.yml
kubectl delete -f kubernetes/fastapi-web-app/fastapi-web-app-service.yml
```

---

## Helm Commands

### Quick Helm Deployment

```bash
# Validate Helm chart
helm lint helm/helm-e-cloud-learniverse

# Dry run to preview deployment
helm install e-cloud helm/helm-e-cloud-learniverse --dry-run --debug

# Install application with Helm
helm install e-cloud helm/helm-e-cloud-learniverse

# Check deployment status
helm status e-cloud
kubectl get all

# Port forward to access application
kubectl port-forward service/fastapi-web-app-service 8002:80

# Access application at http://localhost:8002
```

### Environment-Specific Deployments

```bash
# Development environment
helm install e-cloud-dev helm/helm-e-cloud-learniverse \
  -f helm/helm-e-cloud-learniverse/values-dev.yml

# Staging environment
helm install e-cloud-staging helm/helm-e-cloud-learniverse \
  -f helm/helm-e-cloud-learniverse/values-staging.yml

# Production environment
helm install e-cloud-prod helm/helm-e-cloud-learniverse \
  -f helm/helm-e-cloud-learniverse/values-prod.yml
```

### Helm Management Commands

```bash
# List all releases
helm list

# Upgrade release
helm upgrade e-cloud helm/helm-e-cloud-learniverse

# Rollback to previous version
helm rollback e-cloud

# Uninstall release
helm uninstall e-cloud
```

---

## Useful Commands

### Kubernetes Utilities

```bash
# Check current context
kubectl config current-context

# Switch context
kubectl config use-context kind-mac-cluster-test

# View all resources
kubectl get all

# Check logs
kubectl logs -l app=fastapi-web-app
kubectl logs -l app=postgres

# Kill port-forward processes (macOS)
pkill -f "kubectl port-forward"
```

### Database Commands

```bash
# Connect to PostgreSQL container
kubectl exec -it deployment/postgres-deployment -- psql -U postgres -d e_cloud_learniverse_db

# Install psycopg2 locally
pip install --no-build-isolation --only-binary :all: psycopg2-binary sqlalchemy
```
---

## Commands

- [Docker Commands](DOCKER_COMMANDS.md) - Detailed Docker setup and commands
- [Kubernetes Commands](kubernetes/KUBERNETES_COMMANDS.md) - Kubernetes deployment guide
- [Kind Commands](kubernetes/KIND_COMMANDS.md) - Local Kubernetes cluster setup
- [Helm Commands](helm/HELM_COMMANDS.md) - Complete Helm deployment guide
- [Helm Theory](helm/HELM_THEORY.md) - Helm concepts and built-in variables
- [FastAPI Setup](FASTAPI_README.md) - FastAPI development setup