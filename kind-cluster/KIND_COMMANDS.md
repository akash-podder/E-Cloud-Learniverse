# Kind (Kubernetes in Docker) Commands

Kind Official Guide: [Kind Documentation](https://kind.sigs.k8s.io/docs/user/quick-start/)
```bash
# Make it executable
chmod +x /kind-cluster/kind_install.sh
# Run the installation
./kind-cluster/kind_install.sh
kind version

brew install kubectl
kubectl version
```

### create a kind cluster
--name mac-cluster-test → “Cluster” er Name
--image → without this Tag it will download the “latest” image
```bash
kind create cluster --name mac-cluster-test --image kindest/node:v1.30.6
```

`Three Node (1 Master and 2 Worker) Cluster` Command:
```bash
kind create cluster --name mac-cluster-test --image kindest/node:v1.30.6 --config kind-three-node-config.yml
```

```bash
docker ps
```

Output:
```bash
CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS          PORTS                       NAMES
4e1290227130   kindest/node:v1.30.6   "/usr/local/bin/entr…"   10 minutes ago   Up 10 minutes   127.0.0.1:51962->6443/tcp   mac-cluster-test-control-plane
```

This Config File is AUTOMATICALLY Created by “Kind”... If we are using any Cloud Providers, then we have to download that Config File from the Cloud Providers and put that Config file in that particular Directory
```bash
cat ~/.kube/config
```
  
To “Temporarily” set “kubectl” to Point to Different Config File
```bash
export KUBECONFIG=~/.kube/devconfig
```

To see current Config which the kubectl is pointing to
```bash
kubectl config view
```

Kubectl is Pointing to Currently which “Cluster”
```bash
kubectl config current-context
```

To Switch to another “Cluster”
```bash
kubectl config use-context kind-mac-cluster-test
```

```bash
kubectl config current-context
```

Load `e-cloud-fastapi-docker-image` to locally in "mac-cluster-test"
```bash
kind load docker-image e-cloud-fastapi-docker-image:latest --name mac-cluster-test
```

## `Kind` remove images from Cluster
`crictl` == `docker` command, but it is an Open Source CLI for any `Container Runtime` (example: `CRI-O`, `run-c`)

`crictl` stands for `Container Runtime Interface CLI`.
It’s a command-line tool used to interact directly with the container runtime (like containerd, CRI-O, etc.) that Kubernetes uses under the hood.
```bash
docker exec mac-cluster-test-control-plane crictl rmi docker.io/library/e-cloud-fastapi-docker-image:latest
docker exec mac-cluster-test-control-plane crictl rmi docker.io/library/reactjs-frontend-e-cloud-docker-image:latest
docker exec mac-cluster-test-control-plane crictl rmi docker.io/library/postgres:17
```
Think of it as the Kubernetes-friendly equivalent of docker CLI — but it talks to the CRI layer used by kubelet.

So:
When you run docker ps → it lists Docker containers.

When you run crictl ps → it lists containers managed by Kubernetes (via CRI).