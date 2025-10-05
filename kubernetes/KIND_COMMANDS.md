# Kind (Kubernetes in Docker) Commands

```bash
brew install kind
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