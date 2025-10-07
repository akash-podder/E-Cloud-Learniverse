# Helm (Kubernetes Package Manager)

## 📦 1. Helm Create Project
```bash
cd helm
helm create helm-e-cloud-learniverse
```

Remove the default templates Helm generates (so you can put your own):
```bash
rm -rf helm-e-cloud-learniverse/templates/*
```

Then Copy the `kubernetes` object file into Helm `Template` folder
```bash
cp kubernetes/postgres/postgres-deployment.yml helm/helm-e-cloud-learniverse/templates/
cp kubernetes/postgres/postgres-service.yml helm/helm-e-cloud-learniverse/templates/
cp kubernetes/fastapi-web-app/fastapi-web-app-deployment.yml helm/helm-e-cloud-learniverse/templates/
cp kubernetes/fastapi-web-app/fastapi-web-app-service.yml helm/helm-e-cloud-learniverse/templates/
```

---

## 🔍 2. Validate & Debug Helm Templates

### Dry Run - Validate templates without installing
```bash
helm install e-cloud helm/helm-e-cloud-learniverse --dry-run --debug
```

### Render templates locally to see the final YAML
```bash
helm template e-cloud helm/helm-e-cloud-learniverse
```

### Lint the Helm chart for errors
```bash
helm lint helm/helm-e-cloud-learniverse
```

---

## 📦 3. Package the Helm Chart

Run this from the `helm/` folder (one level above the chart):
```bash
cd helm
helm package helm-e-cloud-learniverse
```

That will generate:
```
helm-e-cloud-learniverse-0.1.0.tgz
```

---

## 🚀 4. Install Helm Chart

### Install from packaged .tgz file
Here, 1st parameter `e-cloud` is the **Release Name** & 2nd parameter is the **Chart package**
```bash
helm install e-cloud helm-e-cloud-learniverse-0.1.0.tgz
```

### Install directly from folder (without packaging) - Recommended for Development
```bash
helm install e-cloud helm/helm-e-cloud-learniverse
```

### Install with custom release name
```bash
helm install my-fastapi-app helm/helm-e-cloud-learniverse
```

---

## 🔄 5. Using Custom Values Files

### Install with custom values file (e.g., values-dev.yml)
```bash
helm install e-cloud helm/helm-e-cloud-learniverse -f helm/helm-e-cloud-learniverse/values-dev.yml
```

### Install with multiple values files (later files override earlier ones)
```bash
helm install e-cloud helm/helm-e-cloud-learniverse \
  -f helm/helm-e-cloud-learniverse/values.yaml \
  -f helm/helm-e-cloud-learniverse/values-dev.yml
```

### Override specific values from command line
```bash
helm install e-cloud helm/helm-e-cloud-learniverse \
  --set fastapi.replicaCount=3 \
  --set postgres.env.postgresPassword=secretpassword
```

### Combine custom values file + command line overrides
```bash
helm install e-cloud helm/helm-e-cloud-learniverse \
  -f helm/helm-e-cloud-learniverse/values-prod.yml \
  --set fastapi.image.tag=v2.0.0
```

---

## 🔄 6. Upgrade Existing Release

### Upgrade with default values.yaml
```bash
helm upgrade e-cloud helm/helm-e-cloud-learniverse
```

### Upgrade with custom values file
```bash
helm upgrade e-cloud helm/helm-e-cloud-learniverse -f helm/helm-e-cloud-learniverse/values-dev.yml
```

### Upgrade with command line overrides
```bash
helm upgrade e-cloud helm/helm-e-cloud-learniverse --set fastapi.replicaCount=5
```

### Install if not exists, upgrade if exists
```bash
helm upgrade --install e-cloud helm/helm-e-cloud-learniverse
```

---

## 🔍 7. Verify Deployment

### List all Helm releases
```bash
helm list
```

### List releases in all namespaces
```bash
helm list --all-namespaces
```

### Get release status
```bash
helm status e-cloud
```

### Get release values
```bash
helm get values e-cloud
```

### Get all values (including defaults)
```bash
helm get values e-cloud --all
```

### Check Kubernetes resources
```bash
kubectl get all
kubectl get pods
kubectl get services
kubectl get deployments
```

---

## 🗑️ 8. Uninstall Helm Release

### Uninstall release
```bash
helm uninstall e-cloud
```

### Uninstall and keep history
```bash
helm uninstall e-cloud --keep-history
```

---

## 📜 9. History & Rollback

### View release history
```bash
helm history e-cloud
```

### Rollback to previous revision
```bash
helm rollback e-cloud
```

### Rollback to specific revision
```bash
helm rollback e-cloud 2
```

---

## 🌍 10. Environment-Specific Deployments

### Create environment-specific values files

**values-dev.yml** (Development environment)
```yaml
fastapi:
  replicaCount: 1
  image:
    tag: dev
    pullPolicy: Always
  env:
    databasePassword: dev-password

postgres:
  env:
    postgresPassword: dev-password
```

**values-staging.yml** (Staging environment)
```yaml
fastapi:
  replicaCount: 2
  image:
    tag: staging
  env:
    databasePassword: staging-password

postgres:
  env:
    postgresPassword: staging-password
```

**values-prod.yml** (Production environment)
```yaml
fastapi:
  replicaCount: 3
  image:
    tag: v1.0.0
    pullPolicy: IfNotPresent
  env:
    databasePassword: super-secret-prod-password

postgres:
  replicaCount: 2
  env:
    postgresPassword: super-secret-prod-password
```

### Deploy to different environments

```bash
# Development
helm install e-cloud-dev helm/helm-e-cloud-learniverse -f helm/helm-e-cloud-learniverse/values-dev.yml

# Staging
helm install e-cloud-staging helm/helm-e-cloud-learniverse -f helm/helm-e-cloud-learniverse/values-staging.yml

# Production
helm install e-cloud-prod helm/helm-e-cloud-learniverse -f helm/helm-e-cloud-learniverse/values-prod.yml
```

---

## 🔐 11. Using Kubernetes Secrets

### Override sensitive values at install time
```bash
helm install e-cloud helm/helm-e-cloud-learniverse \
  --set postgres.env.postgresPassword=$DB_PASSWORD \
  --set fastapi.env.databasePassword=$DB_PASSWORD
```

### Use external secrets (recommended for production)
Use tools like:
- **Sealed Secrets**
- **External Secrets Operator**
- **HashiCorp Vault**

---

## 🧪 12. Testing Commands

### Port-forward to access FastAPI service locally
```bash
kubectl port-forward service/fastapi-web-app-service 8002:80
```

### Access via NodePort (if using NodePort service type)
```bash
# Get the NodePort
kubectl get svc fastapi-web-app-service

# Access at: http://localhost:30004
```

### Check logs
```bash
kubectl logs -l ramos-app-name=fastapi-web-app-e-cloud-pod
kubectl logs -l messi-db-app=postgres-e-cloud-pod
```

---

## 📊 13. Common Helm Commands Cheat Sheet

| Command | Description |
|---------|-------------|
| `helm install <release> <chart>` | Install a chart |
| `helm upgrade <release> <chart>` | Upgrade a release |
| `helm upgrade --install <release> <chart>` | Install or upgrade |
| `helm uninstall <release>` | Uninstall a release |
| `helm list` | List all releases |
| `helm status <release>` | Show release status |
| `helm get values <release>` | Get release values |
| `helm rollback <release> <revision>` | Rollback to revision |
| `helm history <release>` | View release history |
| `helm template <chart>` | Render templates locally |
| `helm lint <chart>` | Lint a chart |
| `helm package <chart>` | Package a chart |

---

## 🚀 14. Quick Start Workflow

```bash
# 1. Validate templates
helm lint helm/helm-e-cloud-learniverse

# 2. Dry run to see what will be deployed
helm install e-cloud helm/helm-e-cloud-learniverse --dry-run --debug

# 3. Install the chart
helm install e-cloud helm/helm-e-cloud-learniverse

# 4. Check status
helm status e-cloud
kubectl get all

# 5. Port forward to access application
kubectl port-forward service/fastapi-web-app-service 8002:80

# 6. Access application at http://localhost:8002
```

---

## 🔄 15. Development Workflow with Custom Values

```bash
# 1. Create values-dev.yml with your development settings

# 2. Install with dev values
helm install e-cloud-dev helm/helm-e-cloud-learniverse -f helm/helm-e-cloud-learniverse/values-dev.yml

# 3. Make changes to templates or values

# 4. Upgrade with new changes
helm upgrade e-cloud-dev helm/helm-e-cloud-learniverse -f helm/helm-e-cloud-learniverse/values-dev.yml

# 5. If something goes wrong, rollback
helm rollback e-cloud-dev
```

---

## 📝 Notes

- Always use `helm lint` before deploying
- Use `--dry-run --debug` to validate changes before applying
- Keep sensitive values in separate files or use Kubernetes secrets
- Use different release names for different environments
- Version your Helm charts properly in `Chart.yaml`
