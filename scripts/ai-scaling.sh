#!/bin/bash

# Script to implement kubectl-ai scaling commands
# This script uses kubectl-ai for AI-assisted scaling operations per spec.md FR-009

set -e  # Exit immediately if a command exits with a non-zero status

echo "Running AI-assisted scaling operations..."

# Check if kubectl-ai is available
if ! command -v kubectl-ai &> /dev/null; then
    echo "Warning: kubectl-ai is not installed. Falling back to standard kubectl scaling."
    echo "To install kubectl-ai: kubectl krew install ai"
    echo "Performing standard scaling operations..."

    # Standard kubectl scaling operations
    kubectl scale deployment todo-frontend-deployment --replicas=1
    kubectl scale deployment todo-backend-deployment --replicas=1
    kubectl scale deployment todo-mcp-server-deployment --replicas=1

    echo "Standard scaling operations completed."
    exit 0
fi

echo "kubectl-ai is available. Running AI-assisted scaling..."

# Get AI recommendations for scaling based on resource usage
echo "Getting AI scaling recommendations..."
kubectl ai suggest scale deployment todo-frontend-deployment
kubectl ai suggest scale deployment todo-backend-deployment
kubectl ai suggest scale deployment todo-mcp-server-deployment

# Apply initial scaling (starting with 1 replica for each)
kubectl ai scale deployment todo-frontend-deployment --replicas=1
kubectl ai scale deployment todo-backend-deployment --replicas=1
kubectl ai scale deployment todo-mcp-server-deployment --replicas=1

# Monitor scaling status
echo "Monitoring scaling status..."
kubectl ai explain deployment todo-frontend-deployment
kubectl ai explain deployment todo-backend-deployment
kubectl ai explain deployment todo-mcp-server-deployment

echo "AI-assisted scaling operations completed successfully!"