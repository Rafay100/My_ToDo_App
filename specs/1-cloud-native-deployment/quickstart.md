# Quickstart Guide: Cloud-Native Todo AI Chatbot

## Prerequisites

- Docker Desktop with Kubernetes enabled
- Minikube (latest version)
- Helm 3.x
- kubectl
- kubectl-ai plugin
- Kagent
- Docker AI Agent (Gordon)

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Start Minikube

```bash
minikube start
```

### 3. Enable required Minikube addons

```bash
minikube addons enable ingress
minikube addons enable metrics-server
```

### 4. Build Docker Images using AI Assistance

```bash
# Navigate to docker directory
cd docker

# Use Gordon AI Agent to optimize Dockerfiles
gordon analyze frontend/Dockerfile
gordon analyze backend/Dockerfile
gordon analyze mcp-server/Dockerfile

# Build and tag images for Minikube
eval $(minikube docker-env)
docker build -t todo-frontend:v1.0.0 -f frontend/Dockerfile .
docker build -t todo-backend:v1.0.0 -f backend/Dockerfile .
docker build -t todo-mcp-server:v1.0.0 -f mcp-server/Dockerfile .
```

### 5. Deploy using Helm and AI Assistance

```bash
# Navigate to charts directory
cd charts/todo-ai-chatbot

# Use kubectl-ai to generate deployment configurations
kubectl-ai suggest helm-values

# Install the Helm chart
helm install todo-ai-chatbot . --values values.yaml

# Verify deployment
kubectl get pods
kubectl get services
```

### 6. Access the Application

```bash
# Get the frontend service URL
minikube service todo-frontend-service --url

# Or access via dashboard
minikube dashboard
```

## AI-Assisted Operations

### Using kubectl-ai for Deployment Management

```bash
# Generate deployment manifests
kubectl-ai generate deployment --image todo-backend:v1.0.0 --name backend

# Scale deployments intelligently
kubectl-ai scale deployment/backend --replicas 2

# Debug deployment issues
kubectl-ai explain pod/backend-pod-name
```

### Using Kagent for Cluster Analysis

```bash
# Analyze cluster health
kagent analyze cluster

# Get resource optimization suggestions
kagent suggest resources

# Monitor deployment performance
kagent monitor deployment/backend
```

## Verification

1. Check that all pods are running:
   ```bash
   kubectl get pods
   ```

2. Verify services are accessible:
   ```bash
   kubectl get services
   ```

3. Check application logs:
   ```bash
   kubectl logs deployment/todo-frontend
   kubectl logs deployment/todo-backend
   kubectl logs deployment/todo-mcp-server
   ```

4. Access the frontend in your browser using the Minikube service URL.

## Troubleshooting

### Common Issues

- **ImagePullBackOff**: Ensure images are built and tagged correctly for Minikube
- **CrashLoopBackOff**: Check application logs for configuration errors
- **Service Unavailable**: Verify service types and port configurations

### AI-Assisted Troubleshooting

```bash
# Use kubectl-ai to diagnose issues
kubectl-ai diagnose pod/problematic-pod-name

# Get optimization suggestions from Kagent
kagent suggest pod/problematic-pod-name
```

## Cleanup

```bash
# Uninstall the Helm release
helm uninstall todo-ai-chatbot

# Stop Minikube
minikube stop

# Optionally delete the cluster
minikube delete
```