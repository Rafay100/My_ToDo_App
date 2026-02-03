# Data Model: Cloud-Native Todo AI Chatbot

## Containerization Entities

### Container Image
- **Description**: Represents a packaged application with all dependencies for Kubernetes deployment
- **Attributes**:
  - name: String (image name)
  - tag: String (version tag)
  - size: Integer (compressed size in MB)
  - layers: Array of Strings (Docker layers)
  - architecture: String (target architecture)
- **Validation**:
  - name must be valid Docker image name format
  - tag must follow semantic versioning or latest

### Helm Chart
- **Description**: Represents a Kubernetes application package with templates and configurations
- **Attributes**:
  - name: String (chart name)
  - version: String (chart version)
  - appVersion: String (application version)
  - templates: Array of Strings (template files)
  - values: Object (configuration values)
  - dependencies: Array of Objects (sub-charts)
- **Validation**:
  - version must follow semantic versioning
  - templates must be valid Kubernetes YAML

### Kubernetes Deployment
- **Description**: Represents a declarative configuration for running application pods
- **Attributes**:
  - name: String (deployment name)
  - replicas: Integer (desired pod count)
  - image: String (container image reference)
  - resources: Object (CPU/memory limits/requests)
  - environment: Object (environment variables)
- **Validation**:
  - replicas must be non-negative
  - image must reference valid container image

### Kubernetes Service
- **Description**: Represents a network abstraction for accessing applications within or outside the cluster
- **Attributes**:
  - name: String (service name)
  - type: Enum ('ClusterIP', 'NodePort', 'LoadBalancer') (service type)
  - ports: Array of Objects (port mappings)
  - selector: Object (pod selector labels)
- **Validation**:
  - ports must have valid port numbers (1-65535)
  - type must be one of allowed values

### Minikube Cluster
- **Description**: Represents a local Kubernetes environment for development and testing
- **Attributes**:
  - name: String (cluster name)
  - driver: String (virtualization driver)
  - nodes: Integer (number of nodes)
  - kubernetesVersion: String (Kubernetes version)
  - resources: Object (allocated CPU/memory/storage)
- **Validation**:
  - kubernetesVersion must be valid Kubernetes version
  - resources must be positive values

## Relationships
- Helm Chart 1---* Kubernetes Deployment (one chart can define multiple deployments)
- Kubernetes Deployment 1---* Container Image (deployment uses image)
- Kubernetes Service *---* Kubernetes Deployment (services expose deployments)
- Minikube Cluster 1---* Kubernetes Deployment (deployments run on cluster)

## Kubernetes Resource Specifications

### Frontend Deployment
- Replicas: 1 (for local testing)
- Resources: 256Mi memory request/limit, 250m CPU request/limit
- Environment: NEXT_PUBLIC_API_URL pointing to backend service

### Backend Deployment
- Replicas: 1 (for local testing)
- Resources: 512Mi memory request/limit, 500m CPU request/limit
- Environment: Database connection details, OpenAI API key

### MCP Server Deployment
- Replicas: 1 (for local testing)
- Resources: 256Mi memory request/limit, 250m CPU request/limit
- Environment: Connection to database and other services

### Services
- Frontend: NodePort type to allow external access
- Backend: ClusterIP type for internal access only
- MCP Server: ClusterIP type for internal access only