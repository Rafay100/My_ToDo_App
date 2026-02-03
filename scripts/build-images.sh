#!/bin/bash

# Script to build and tag Docker images for Minikube
# This script uses Gordon AI Agent for optimization where available

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting Docker image build process..."

# Ensure Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Set Docker environment to point to Minikube
echo "Setting Docker environment to Minikube..."
eval $(minikube docker-env)

# Build frontend image
echo "Building frontend Docker image..."
if command -v gordon &> /dev/null; then
    echo "Using Gordon AI Agent for Docker optimization..."
    # Analyze and optimize Dockerfile if Gordon is available
    gordon analyze docker/frontend/Dockerfile || echo "Gordon analysis skipped"
fi

docker build -t todo-frontend:latest -t todo-frontend:v1.0.0 -f docker/frontend/Dockerfile . || {
    echo "Error: Failed to build frontend image"
    exit 1
}

# Build backend image
echo "Building backend Docker image..."
if command -v gordon &> /dev/null; then
    echo "Using Gordon AI Agent for Docker optimization..."
    gordon analyze docker/backend/Dockerfile || echo "Gordon analysis skipped"
fi

docker build -t todo-backend:latest -t todo-backend:v1.0.0 -f docker/backend/Dockerfile . || {
    echo "Error: Failed to build backend image"
    exit 1
}

# Build MCP server image
echo "Building MCP server Docker image..."
if command -v gordon &> /dev/null; then
    echo "Using Gordon AI Agent for Docker optimization..."
    gordon analyze docker/mcp-server/Dockerfile || echo "Gordon analysis skipped"
fi

docker build -t todo-mcp-server:latest -t todo-mcp-server:v1.0.0 -f docker/mcp-server/Dockerfile . || {
    echo "Error: Failed to build MCP server image"
    exit 1
}

echo "All Docker images built and tagged successfully!"
echo "Images available in Minikube registry:"
docker images | grep -E "(todo-frontend|todo-backend|todo-mcp-server)"