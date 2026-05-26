### Apply URL Rewrite Config
```
kubectl apply -f rewrite-httproute.yaml
```

### CURL Request
Get the `Hostname` from Yaml file where hostname: `path.rewrite.example`
```
curl -L -vvv --header "Host: path.rewrite.example" "https://localhost:8888/get/origin/path/extra"
```
