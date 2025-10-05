# Kubernetes Basic Commands

svc == Shortform of "service"

```bash
kubectl create ns example-apps → Creating Namespace called “example-apps”
kubectl -n example-apps create deployment webserver --image=nginx --port=80
kubectl -n example-apps get deploy
kubectl -n example-apps get pods
kubectl -n example-apps get pods -o wide → More Info for Pods
kubectl -n example-apps create service clusterip webserver --tcp 80:80
kubectl -n example-apps get service
kubectl -n example-apps port-forward svc/webserver 8000:80
```

# Project Commands
At first get the Current Cluster Name what "kubctl" is pointing to

```bash
kubectl config current-context
```

Load `e-cloud-fastapi-docker-image` to locally in `mac-cluster-test`
```bash
kind load docker-image e-cloud-fastapi-docker-image:latest --name mac-cluster-test
```

```bash
kubectl apply -f kubernetes/postgres/postgres-deployment.yml       
kubectl apply -f kubernetes/postgres/postgres-svc.yml
kubectl apply -f kubernetes/fastapi-web-app/fastapi-web-app-pod.yml 
```

```bash
kubectl delete -f kubernetes/postgres/postgres-deployment.yml       
kubectl delete -f kubernetes/postgres/postgres-svc.yml
kubectl delete -f kubernetes/fastapi-web-app/fastapi-web-app-pod.yml 
```

Port Forward to 8002 to 9998
```bash
kubectl port-forward pod/e-cloud-learniverse 8002:9998
```