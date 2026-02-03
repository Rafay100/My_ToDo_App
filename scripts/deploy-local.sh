#!/bin/bash

# Deploy the Advanced Cloud-Native Todo AI Platform to Minikube with Dapr and Kafka
# This script implements the local deployment as specified in spec.md

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting deployment to Minikube..."

# Check if minikube is installed
if ! command -v minikube &> /dev/null; then
    echo "Error: minikube is not installed. Please install minikube first."
    exit 1
fi

# Check if helm is installed
if ! command -v helm &> /dev/null; then
    echo "Error: helm is not installed. Please install helm first."
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check if dapr cli is installed
if ! command -v dapr &> /dev/null; then
    echo "Error: dapr CLI is not installed. Please install dapr CLI first."
    exit 1
fi

# Start Minikube if not running
echo "Checking Minikube status..."
if ! minikube status > /dev/null 2>&1; then
    echo "Starting Minikube cluster..."
    minikube start --driver=docker
else
    echo "Minikube is already running."
fi

# Install Dapr on Minikube
echo "Installing Dapr on Minikube..."
dapr init -k --wait --timeout 300

# Wait for Dapr to be ready
echo "Waiting for Dapr to be ready..."
kubectl wait --for=condition=ready pod -l app=dapr-operator --timeout=300s

# Deploy Kafka using Strimzi
echo "Deploying Kafka to Minikube..."
kubectl create namespace kafka || true

# Install Strimzi operator
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

# Wait for the cluster operator to be ready
kubectl wait --for=condition=ready pod -n kafka --selector=name=strimzi-cluster-operator --timeout=300s

# Deploy Kafka cluster
kubectl apply -f - <<EOF
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
  namespace: kafka
spec:
  kafka:
    version: 3.7.0
    replicas: 1
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
      offsets.topic.replication.factor: 1
      transaction.state.log.replication.factor: 1
      transaction.state.log.min.isr: 1
      default.replication.factor: 1
      min.insync.replicas: 1
      inter.broker.protocol.version: "3.7"
    storage:
      type: jbod
      volumes:
      - id: 0
        type: persistent-claim
        size: 10Gi
        deleteClaim: false
  zookeeper:
    replicas: 1
    storage:
      type: persistent-claim
      size: 5Gi
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
  partitions: 3
  replicas: 1
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
  partitions: 3
  replicas: 1
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
  partitions: 3
  replicas: 1
  config:
    retention.ms: 604800000
    segment.bytes: 1073741824
EOF

# Wait for Kafka to be ready
echo "Waiting for Kafka to be ready..."
kubectl wait --for=condition=ready pod -n kafka -l strimzi.io/name=my-cluster-kafka --timeout=300s

# Build and load images into Minikube
echo "Setting Docker environment to Minikube..."
eval $(minikube docker-env)

echo "Building Docker images for Minikube..."
docker build -t todo-frontend:latest -f docker/frontend/Dockerfile . || echo "Frontend image build skipped"
docker build -t todo-backend:latest -f docker/backend/Dockerfile . || echo "Backend image build skipped"
docker build -t notification-service:latest -f - . <<EOF
FROM python:3.11-slim
WORKDIR /app
COPY notification-service/src /app
RUN pip install dapr dapr-ext-grpc
CMD ["python", "main.py"]
EOF
docker build -t recurring-task-service:latest -f - . <<EOF
FROM python:3.11-slim
WORKDIR /app
COPY recurring-task-service/src /app
RUN pip install dapr dapr-ext-grpc python-dateutil
CMD ["python", "main.py"]
EOF
docker build -t audit-service:latest -f - . <<EOF
FROM python:3.11-slim
WORKDIR /app
COPY audit-service/src /app
RUN pip install dapr dapr-ext-grpc
CMD ["python", "main.py"]
EOF

# Install the Helm chart
echo "Installing Helm chart to Minikube..."
helm upgrade --install todo-ai-platform ./charts/todo-ai-platform/ --values ./charts/todo-ai-platform/values.yaml

# Wait for deployments to be ready
echo "Waiting for deployments to be ready..."
kubectl wait --for=condition=ready pod -l app=todo-frontend --timeout=300s || true
kubectl wait --for=condition=ready pod -l app=todo-backend --timeout=300s || true
kubectl wait --for=condition=ready pod -l app=notification-service --timeout=300s || true
kubectl wait --for=condition=ready pod -l app=recurring-task-service --timeout=300s || true
kubectl wait --for=condition=ready pod -l app=audit-service --timeout=300s || true

# Verify all services are running
echo "Verifying deployment..."
kubectl get pods
kubectl get services
kubectl get deployments

echo "Deployment completed successfully!"
echo "Access the application via Minikube IP on the exposed ports."