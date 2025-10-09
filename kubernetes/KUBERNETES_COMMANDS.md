# Kubernetes Basic Commands

`svc` == Shortform of "service"

`-n` Flag == Namespace Flag

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
At first get the Current Cluster Name what "kubectl" is pointing to

## Commands for "load" image in "Kind" Cluster
```bash
kubectl config current-context
```

### First build `Backend` image and load in `kind` Cluster
```bash
sudo docker build --tag e-cloud-fastapi-docker-image ./backend
```

Load `e-cloud-fastapi-docker-image` to locally in `mac-cluster-test`
```bash
kind load docker-image e-cloud-fastapi-docker-image:latest --name mac-cluster-test
```

### Build `Frontend` image and load in `kind` Cluster
```bash
 sudo docker build --build-arg ENV_FILE=kubernetes -t reactjs-frontend-e-cloud-docker-image:kubernetes ./frontend/e-cloud-learniverse-frontend-react
```

Load `reactjs-frontend-e-cloud-docker-image` to locally in `mac-cluster-test`
```bash
kind load docker-image reactjs-frontend-e-cloud-docker-image:kubernetes --name mac-cluster-test
```

## `Kind` remove images from Cluster
`crictl` == `docker` command, but it is an Open Source CLI for any `Container Runtime` (example: `CRI-O`, `run-c`)

`crictl` stands for `Container Runtime Interface CLI`.
```bash
docker exec mac-cluster-test-control-plane crictl rmi docker.io/library/e-cloud-fastapi-docker-image:latest
docker exec mac-cluster-test-control-plane crictl rmi docker.io/library/reactjs-frontend-e-cloud-docker-image:latest
docker exec mac-cluster-test-control-plane crictl rmi docker.io/library/postgres:17
```

## Commands for "Pod" Object
```bash
kubectl apply -f kubernetes/postgres/postgres-deployment.yml       
kubectl apply -f kubernetes/postgres/postgres-service.yml

kubectl apply -f kubernetes/fastapi-web-app/fastapi-web-app-pod.yml
kubectl apply -f kubernetes/fastapi-web-app/fastapi-web-app-service.yml

kubectl apply -f kubernetes/frontend-react-app/reactjs-frontend-app-pod.yml
kubectl apply -f kubernetes/frontend-react-app/reactjs-frontend-app-service.yml
```

To delete all the Kubernetes Objects
```bash
kubectl delete -f kubernetes/postgres/postgres-deployment.yml       
kubectl delete -f kubernetes/postgres/postgres-service.yml

kubectl delete -f kubernetes/fastapi-web-app/fastapi-web-app-pod.yml
kubectl delete -f kubernetes/fastapi-web-app/fastapi-web-app-service.yml

kubectl delete -f kubernetes/frontend-react-app/reactjs-frontend-app-pod.yml
kubectl delete -f kubernetes/frontend-react-app/reactjs-frontend-app-service.yml
```

Port Forward the `Backend Service` for locahost 8002 to Pod's 9998
```bash
kubectl port-forward pod/e-cloud-learniverse 8002:9998
```

Port Forward the `Frontend Service` for localhost 3000 to Service's 3000
```bash
kubectl port-forward service/reactjs-frontend-app-service 3000:3000
```

## Commands for "Deployment" Object
```bash
kubectl apply -f kubernetes/postgres/postgres-deployment.yml       
kubectl apply -f kubernetes/postgres/postgres-service.yml

kubectl apply -f kubernetes/fastapi-web-app/fastapi-web-app-deployment.yml
kubectl apply -f kubernetes/fastapi-web-app/fastapi-web-app-service.yml

kubectl apply -f kubernetes/frontend-react-app/reactjs-frontend-app-deployment.yml
kubectl apply -f kubernetes/frontend-react-app/reactjs-frontend-app-service.yml
```

To delete all the Kubernetes Objects
```bash
kubectl delete -f kubernetes/postgres/postgres-deployment.yml       
kubectl delete -f kubernetes/postgres/postgres-service.yml

kubectl delete -f kubernetes/fastapi-web-app/fastapi-web-app-deployment.yml
kubectl delete -f kubernetes/fastapi-web-app/fastapi-web-app-service.yml

kubectl delete -f kubernetes/frontend-react-app/reactjs-frontend-app-deployment.yml
kubectl delete -f kubernetes/frontend-react-app/reactjs-frontend-app-service.yml
```

Port Forward the `Backend Service` for locahost 8002 to Service Container's 80
```bash
kubectl port-forward service/fastapi-web-app-service 8002:80
```

Port Forward the `Frontend Service` for localhost 3000 to Service's 3000
```bash
kubectl port-forward service/reactjs-frontend-app-service 3000:3000
```

### Kill Process
You can kill all running kubectl port-forward processes with a single command in `MacOS`:
```bash
pkill -f "kubectl port-forward"
```