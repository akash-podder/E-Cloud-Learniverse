### Deploy 2nd Backend
```
cd backend-2/
kubectl apply -f svc_account.yaml
kubectl apply -f deploy.yaml
kubectl apply -f svc.yaml
kubectl get all
```

### Apply Traffic Splitting Config
```
kubectl apply -f httproute_traffic_splitting.yaml
```

### CURL Request
Get the `Hostname` from Yaml file where hostname: `backends.example`
```
curl -L -vvv --header "Host: backends.example" "https://localhost:8888/get/origin/path/extra"
```