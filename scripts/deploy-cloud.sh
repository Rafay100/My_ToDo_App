#!/bin/bash

# Deploy the Advanced Cloud-Native Todo AI Platform to cloud Kubernetes (AKS/GKE/OKE)
# This script implements the cloud deployment as specified in spec.md

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting deployment to cloud Kubernetes..."

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check if helm is installed
if ! command -v helm &> /dev/null; then
    echo "Error: helm is not installed. Please install helm first."
    exit 1
fi

# Check if dapr cli is installed
if ! command -v dapr &> /dev/null; then
    echo "Error: dapr CLI is not installed. Please install dapr CLI first."
    exit 1
fi

# The script expects that you have already configured kubectl to point to your cloud cluster
echo "Verifying kubectl connection to cloud cluster..."
kubectl cluster-info

# Verify that we're connected to the correct cluster
read -p "Continue with deployment to this cluster? (yes/no): " -r
if [[ ! $REPLY =~ ^yes$ ]]; then
    echo "Deployment cancelled."
    exit 0
fi

# Install Dapr on cloud Kubernetes
echo "Installing Dapr on cloud Kubernetes..."
dapr init -k --wait --timeout 300

# Wait for Dapr to be ready
echo "Waiting for Dapr to be ready..."
kubectl wait --for=condition=ready pod -l app=dapr-operator --timeout=300s

# Deploy Kafka using Strimzi for cloud
echo "Deploying Kafka to cloud cluster..."
kubectl create namespace kafka || true

# Install Strimzi operator
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

# Wait for the cluster operator to be ready
kubectl wait --for=condition=ready pod -n kafka --selector=name=strimzi-cluster-operator --timeout=300s

# Deploy Kafka cluster for cloud (with appropriate sizing for production)
kubectl apply -f - <<EOF
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
  namespace: kafka
spec:
  kafka:
    version: 3.7.0
    replicas: 3  # More replicas for production
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    config:
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 2
      default.replication.factor: 3
      min.insync.replicas: 2
      inter.broker.protocol.version: "3.7"
    storage:
      type: jbod
      volumes:
      - id: 0
        type: persistent-claim
        size: 100Gi  # Larger storage for production
        deleteClaim: false
  zookeeper:
    replicas: 3  # More replicas for production
    storage:
      type: persistent-claim
      size: 20Gi
      deleteClaim: false
  entityOperator:
    topicOperator: {}
    userOperator: {}
EOF

# Deploy Kafka topics
kubectl apply -f - <<EOF
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: task-events
  namespace: kafka
  labels:
    strimzi.io/cluster: my-cluster
spec:
  partitions: 10  # More partitions for production
  replicas: 3
  config:
    retention.ms: 604800000
    segment.bytes: 1073741824
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: reminders
  namespace: kafka
  labels:
    strimzi.io/cluster: my-cluster
spec:
  partitions: 10  # More partitions for production
  replicas: 3
  config:
    retention.ms: 604800000
    segment.bytes: 1073741824
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: task-updates
  namespace: kafka
  labels:
    strimzi.io/cluster: my-cluster
spec:
  partitions: 10  # More partitions for production
  replicas: 3
  config:
    retention.ms: 604800000
    segment.bytes: 1073741824
EOF

# Wait for Kafka to be ready
echo "Waiting for Kafka to be ready..."
kubectl wait --for=condition=ready pod -n kafka -l strimzi.io/name=my-cluster-kafka --timeout=600s

# Pull images from container registry (assuming they're already built and pushed)
echo "Using pre-built images from container registry..."

# Install the Helm chart with cloud-specific values
echo "Installing Helm chart to cloud cluster..."
helm upgrade --install todo-ai-platform ./charts/todo-ai-platform/ --values ./charts/todo-ai-platform/values.yaml \
  --set frontend.replicaCount=3 \
  --set backend.replicaCount=3 \
  --set notificationService.replicaCount=2 \
  --set recurringTaskService.replicaCount=2 \
  --set auditService.replicaCount=2

# Wait for deployments to be ready
echo "Waiting for deployments to be ready..."
kubectl wait --for=condition=ready pod -l app=todo-frontend --timeout=600s || true
kubectl wait --for=condition=ready pod -l app=todo-backend --timeout=600s || true
kubectl wait --for=condition=ready pod -l app=notification-service --timeout=600s || true
kubectl wait --for=condition=ready pod -l app=recurring-task-service --timeout=600s || true
kubectl wait --for=condition=ready pod -l app=audit-service --timeout=600s || true

# Expose services externally if needed
echo "Exposing services externally..."
kubectl patch service todo-ai-platform-frontend-svc -p '{"spec":{"type":"LoadBalancer"}}' || true

# Verify all services are running
echo "Verifying deployment..."
kubectl get pods
kubectl get services
kubectl get deployments

# Get external IPs
echo "External access information:"
kubectl get svc todo-ai-platform-frontend-svc -o jsonpath='{.status.loadBalancer.ingress[0].ip}' || echo "Frontend service external IP not available yet"

echo "Cloud deployment completed successfully!"
echo "Monitor the LoadBalancer service to get the external IP for frontend access."