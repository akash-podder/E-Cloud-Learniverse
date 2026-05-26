# Installation

### Intall Gateway API CRDs and ENVOY Gateway and CRDs
```
helm install eg oci://docker.io/envoyproxy/gateway-helm --version v1.6.1 -n envoy-gateway-system --create-namespace
```

### Check Pods
```
kubectl get pods -n envoy-gateway-system
```

### To Check NEW CRDs
```
kubectl get crds -A
```

### Check the status
```
kubectl wait --timeout=5m -n envoy-gateway-system deployment/envoy-gateway --for=condition=Available
```
