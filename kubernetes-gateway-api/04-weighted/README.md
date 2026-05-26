### Apply HTTP Weighted Route Config
```
kubectl apply -f httproute_weighted.yaml
```

### CURL Request
Get the `Hostname` from Yaml file where hostname: `backends.example`
```
curl -L -vvv --header "Host: backends.example" "https://localhost:8888/get/origin/path/extra"
```