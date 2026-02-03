#!/bin/bash

# Script to deploy Todo AI Chatbot to Minikube using Helm
# This script implements the deployment as specified in spec.md FR-006

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

# Start Minikube if not running
echo "Checking Minikube status..."
if ! minikube status > /dev/null 2>&1; then
    echo "Starting Minikube cluster..."
    minikube start --driver=docker
else
    echo "Minikube is already running."
fi

# Set Docker environment to point to Minikube
echo "Setting Docker environment to Minikube..."
eval $(minikube docker-env)

# Build images if they don't exist
echo "Building Docker images for Minikube registry..."
./scripts/build-images.sh

# Wait a moment for the Docker environment to be properly set
sleep 2

# Navigate to charts directory and install the Helm chart
echo "Installing Helm chart to Minikube..."
helm upgrade --install todo-ai-chatbot ./charts/todo-ai-chatbot/ --values ./charts/todo-ai-chatbot/values.yaml

# Wait for deployments to be ready
echo "Waiting for deployments to be ready..."
kubectl wait --for=condition=ready pod -l app=todo-frontend --timeout=300s
kubectl wait --for=condition=ready pod -l app=todo-backend --timeout=300s
kubectl wait --for=condition=ready pod -l app=todo-mcp-server --timeout=300s

# Expose frontend service
echo "Exposing frontend service..."
kubectl expose deployment todo-frontend-deployment --type=NodePort --port=3000 --name=todo-frontend-service --dry-run=client -o yaml | kubectl apply -f -
kubectl patch service todo-frontend-service -p '{"spec":{"type":"NodePort"}}'

# Get the NodePort for frontend
FRONTEND_PORT=$(kubectl get service todo-frontend-service -o jsonpath='{.spec.ports[0].nodePort}')
echo "Frontend is available at: $(minikube ip):${FRONTEND_PORT}"

# Verify all services are running
echo "Verifying deployment..."
kubectl get pods
kubectl get services
kubectl get deployments

echo "Deployment completed successfully!"
echo "Access the application at: $(minikube ip):${FRONTEND_PORT}"