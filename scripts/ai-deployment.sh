#!/bin/bash

# Script to implement kubectl-ai deployment commands
# This script uses kubectl-ai for AI-assisted deployment operations per spec.md FR-009

set -e  # Exit immediately if a command exits with a non-zero status

echo "Running AI-assisted deployment operations..."

# Check if kubectl-ai is available
if ! command -v kubectl-ai &> /dev/null; then
    echo "Warning: kubectl-ai is not installed. Falling back to standard kubectl operations."
    echo "To install kubectl-ai: kubectl krew install ai"
    echo "Attempting standard deployment verification..."

    # Standard kubectl operations for deployment verification
    kubectl get deployments
    kubectl get pods
    kubectl get services
    exit 0
fi

echo "kubectl-ai is available. Running AI-assisted operations..."

# Generate deployment suggestions
echo "Getting AI deployment analysis..."
kubectl ai explain -f charts/todo-ai-chatbot/templates/frontend-deployment.yaml
kubectl ai explain -f charts/todo-ai-chatbot/templates/backend-deployment.yaml
kubectl ai explain -f charts/todo-ai-chatbot/templates/mcp-server-deployment.yaml

# Get AI recommendations for the current deployment
echo "Getting deployment recommendations..."
kubectl ai recommend --namespace default

# Generate AI-assisted deployment commands if needed
echo "AI deployment operations completed successfully!"