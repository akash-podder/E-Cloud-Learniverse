# Helm Theory

## Built-in Helm Variables

Some values are automatically injected by Helm at runtime. They're not in your `values.yaml` file.

Helm provides built-in variables that are always available in templates:

### Built-in Helm Objects

- **`.Release.Name`** - The release name you specify when running `helm install <name>`
  - Example: `helm install e-cloud ...` → `.Release.Name = e-cloud`
- **`.Release.Namespace`** - The namespace where you're installing
  - Default: `default`
  - Or specify: `helm install e-cloud ... --namespace production`
- **`.Release.Service`** - Always `Helm` (the service doing the release)
- **`.Chart`** - Metadata from `Chart.yaml` file
  - `.Chart.Name`
  - `.Chart.Version`
  - `.Chart.AppVersion`
- **`.Values`** - Values from `values.yaml` (or custom values files)
- **`.Template`** - Info about current template being executed
  - `.Template.Name`
  - `.Template.BasePath`
- **`.Capabilities`** - Info about Kubernetes cluster
  - `.Capabilities.KubeVersion`

### Example Usage

So when you run:
```bash
helm install my-app helm/helm-e-cloud-learniverse --namespace production
```

Helm automatically sets:
- `.Release.Name = my-app`
- `.Release.Namespace = production`

> **Note:** No configuration needed - Helm provides these automatically!