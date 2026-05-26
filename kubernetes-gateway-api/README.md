# Learn Gateway API using Envoy Gateway
Notes for YouTube tutorial on Gateway API --> https://youtu.be/EG27AzlHolU?si=XaQMXkGT3m4K7yv6
Github Link --> https://github.com/iam-veeramalla/kubernetes-gateway-api


# Commands in Sequence

### Install Kubernetes Gateway API (Envoy) first
Go to this Directory and Follow the necessary instructions in `README.md`
```
cd 00-install/
```

## Deploy
Go to this Directory and Follow the necessary instructions in `README.md`
```
cd 01-basic-deploy/
```

### Create Service Account
```
kubectl apply -f svc_account.yaml
```

### Create Deployment
```
kubectl apply -f deploy.yaml
kubectl get pods
```

### Create Service
```
kubectl apply -f svc.yaml
kubectl get svc
```

### Check the Applciation POD and logs
```
kubectl get svc
docker ps
docker exec -it <CONTAINER_ID> /bin/bash
curl <IP_ADDRESS_SERVICE>:3000
```

### Create GatewayClass, Gateway and HTTPRoute
```
kubectl apply -f gateway_class.yaml
kubectl apply -f gateway.yaml
kubectl apply -f httproute.yaml
```

### To see "Envoy" Load Balancer has been created
```
kubectl get pods -n envoy-gateway-system
kubectl get svc -n envoy-gateway-system
```

### Port Forwarding Load Balancer
```
kubectl port-forward svc/envoy-default-eg-e41e7dd 9090:80 -n envoy-gateway-system --address 0.0.0.0
```