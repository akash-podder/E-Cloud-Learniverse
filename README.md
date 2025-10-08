# E-Cloud-Learniverse

## Project Overview

**E-Cloud-Learniverse** is a comprehensive end-to-end web application that demonstrates modern cloud-native development practices and container orchestration. This project showcases the complete journey from development to deployment using industry-standard tools and technologies.

#### To Clone the Repository
```bash
git clone https://github.com/akash-podder/E-Cloud-Learniverse.git
```

### Key Features & Achievements

- **End-to-End Web Application**: Developed a complete web application with FastAPI backend, ReactJS Frontend and PostgreSQL database
- **Containerization**: Containerized with Docker for consistent deployments and scalability
- **Kubernetes Orchestration**: Deployed on Kubernetes using Helm charts, demonstrating expertise in container orchestration
- **Cloud-Native DevOps**: Implements modern DevOps practices with cloud-native technologies

### Technologies Used

- **Frontend**: React.js with Vite (Modern web UI framework)
- **Backend**: FastAPI (Python web framework)
- **Database**: PostgreSQL 17
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Kubernetes
- **Package Management**: Helm Charts

---

## Quick Start

### Prerequisites

- Python 3.8+, Node 22.0+
- Docker, Kubernetes (kubectl), Helm 3.x
- Kind (for local development)

### Local Development Setup

1. **Clone & Setup**
   ```bash
   git clone https://github.com/akash-podder/E-Cloud-Learniverse.git
   cd E-Cloud-Learniverse
   
   # Backend setup
   python -m venv my_venv
   source my_venv/bin/activate
   pip install -r backend/requirements.txt
   
   # Frontend setup
   cd frontend/e-cloud-learniverse-frontend-react
   npm install
   ```

2. **Run Applications**
   ```bash
   # Backend (in terminal 1)
   cd backend && fastapi dev main.py
   
   # Frontend (in terminal 2)
   cd frontend/e-cloud-learniverse-frontend-react && npm run dev
   ```

---

## Docker Quick Start

```bash
# Build images
sudo docker build --tag e-cloud-fastapi-docker-image ./backend
sudo docker build --tag reactjs-frontend-e-cloud-docker-image ./frontend/e-cloud-learniverse-frontend-react

# Run with Docker Compose
sudo docker-compose up --build
```

See [Docker Commands](DOCKER_COMMANDS.md) for detailed setup.

---

## Kubernetes Quick Start

```bash
# Setup Kind cluster
kind create cluster --name mac-cluster-test --image kindest/node:v1.30.6

# Load images
kind load docker-image e-cloud-fastapi-docker-image:latest --name mac-cluster-test
kind load docker-image reactjs-frontend-e-cloud-docker-image:latest --name mac-cluster-test

# Deploy all components
kubectl apply -f kubernetes/postgres/
kubectl apply -f kubernetes/fastapi-web-app/
kubectl apply -f kubernetes/frontend-react-app/

# Access applications
kubectl port-forward service/fastapi-web-app-service 8002:80 &
kubectl port-forward service/reactjs-frontend-app-service 3000:3000 &
```

See [Kubernetes Commands](kubernetes/KUBERNETES_COMMANDS.md) for detailed instructions.

---

## Helm Quick Start

```bash
# Deploy with Helm
helm install e-cloud helm/helm-e-cloud-learniverse

# Check status
helm status e-cloud

# Port forward
kubectl port-forward service/fastapi-web-app-service 8002:80
```

See [Helm Commands](helm/HELM_COMMANDS.md) for complete guide.

---

## Application Access

- **Frontend**: http://localhost:3000 (React.js UI)
- **Backend API**: http://localhost:8002/api (FastAPI)
- **API Docs**: http://localhost:8002/docs (Swagger UI)

### Quick Commands

```bash
# View all resources
kubectl get all

# Kill port-forwards
pkill -f "kubectl port-forward"

# Database access
kubectl exec -it deployment/postgres-deployment -- psql -U postgres -d e_cloud_learniverse_db
```
---

## Commands

- [Docker Commands](DOCKER_COMMANDS.md) - Detailed Docker setup and commands
- [Kubernetes Commands](kubernetes/KUBERNETES_COMMANDS.md) - Kubernetes deployment guide
- [Kind Commands](kubernetes/KIND_COMMANDS.md) - Local Kubernetes cluster setup
- [Helm Commands](helm/HELM_COMMANDS.md) - Complete Helm deployment guide
- [Helm Theory](helm/HELM_THEORY.md) - Helm concepts and built-in variables
- [FastAPI Setup](backend/FASTAPI_README.md) - FastAPI development setup