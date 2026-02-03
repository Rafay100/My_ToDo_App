#!/bin/bash

# Script to implement kubectl-ai debugging commands
# This script uses kubectl-ai for AI-assisted debugging operations per spec.md FR-009

set -e  # Exit immediately if a command exits with a non-zero status

echo "Running AI-assisted debugging operations..."

# Check if kubectl-ai is available
if ! command -v kubectl-ai &> /dev/null; then
    echo "Warning: kubectl-ai is not installed. Falling back to standard debugging."
    echo "To install kubectl-ai: kubectl krew install ai"
    echo "Performing standard debugging operations..."

    # Standard debugging operations
    kubectl get pods
    kubectl describe pods
    kubectl logs deployment/todo-frontend-deployment
    kubectl logs deployment/todo-backend-deployment
    kubectl logs deployment/todo-mcp-server-deployment

    exit 0
fi

echo "kubectl-ai is available. Running AI-assisted debugging..."

# Get AI analysis of current deployments
echo "Getting AI debugging analysis..."
kubectl ai debug pod -l app=todo-frontend
kubectl ai debug pod -l app=todo-backend
kubectl ai debug pod -l app=todo-mcp-server

# Get AI explanation of deployment status
echo "Getting AI explanations for deployments..."
kubectl ai explain deployment todo-frontend-deployment
kubectl ai explain deployment todo-backend-deployment
kubectl ai explain deployment todo-mcp-server-deployment

# Get AI troubleshooting suggestions
echo "Getting AI troubleshooting suggestions..."
kubectl ai suggest troubleshoot -l app=todo-frontend
kubectl ai suggest troubleshoot -l app=todo-backend
kubectl ai suggest troubleshoot -l app=todo-mcp-server

echo "AI-assisted debugging operations completed successfully!"