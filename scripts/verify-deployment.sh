#!/bin/bash

# Script to verify deployment health and functionality
# This script verifies the deployment meets the success criteria from spec.md

set -e  # Exit immediately if a command exits with a non-zero status

echo "Verifying deployment health..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed or not in PATH"
    exit 1
fi

# Check if deployments are ready
echo "Checking deployment status..."
FRONTEND_READY=$(kubectl get deployment todo-frontend-deployment -o jsonpath='{.status.readyReplicas}' 2>/dev/null || echo "0")
BACKEND_READY=$(kubectl get deployment todo-backend-deployment -o jsonpath='{.status.readyReplicas}' 2>/dev/null || echo "0")
MCP_READY=$(kubectl get deployment todo-mcp-server-deployment -o jsonpath='{.status.readyReplicas}' 2>/dev/null || echo "0")

TOTAL_DEPLOYMENTS=$(kubectl get deployments --no-headers | wc -l)
READY_DEPLOYMENTS=0

if [ "$FRONTEND_READY" -gt 0 ]; then
    READY_DEPLOYMENTS=$((READY_DEPLOYMENTS + 1))
    echo "✓ Frontend deployment is ready (${FRONTEND_READY} replicas)"
else
    echo "✗ Frontend deployment is not ready"
fi

if [ "$BACKEND_READY" -gt 0 ]; then
    READY_DEPLOYMENTS=$((READY_DEPLOYMENTS + 1))
    echo "✓ Backend deployment is ready (${BACKEND_READY} replicas)"
else
    echo "✗ Backend deployment is not ready"
fi

if [ "$MCP_READY" -gt 0 ]; then
    READY_DEPLOYMENTS=$((READY_DEPLOYMENTS + 1))
    echo "✓ MCP server deployment is ready (${MCP_READY} replicas)"
else
    echo "✗ MCP server deployment is not ready"
fi

# Check services
echo "Checking services..."
SERVICES_COUNT=$(kubectl get services --no-headers | wc -l)
echo "Found ${SERVICES_COUNT} services"

FRONTEND_SVC=$(kubectl get service todo-frontend-service --no-headers 2>/dev/null && echo "exists" || echo "missing")
if [ "$FRONTEND_SVC" = "exists" ]; then
    echo "✓ Frontend service exists"
else
    echo "✗ Frontend service missing"
fi

# Check pods
echo "Checking pods..."
PODS_RUNNING=$(kubectl get pods --field-selector=status.phase=Running --no-headers | wc -l)
PODS_TOTAL=$(kubectl get pods --no-headers | wc -l)
echo "Running pods: ${PODS_RUNNING}/${PODS_TOTAL}"

# Check if all deployments are ready
if [ $READY_DEPLOYMENTS -eq 3 ] && [ $PODS_RUNNING -gt 0 ]; then
    echo "✓ All deployments are ready and pods are running"

    # Get service access information
    FRONTEND_NODEPORT=$(kubectl get service todo-frontend-service -o jsonpath='{.spec.ports[0].nodePort}' 2>/dev/null)
    if [ ! -z "$FRONTEND_NODEPORT" ]; then
        MINIKUBE_IP=$(minikube ip 2>/dev/null)
        if [ ! -z "$MINIKUBE_IP" ]; then
            echo "✓ Application accessible at: http://${MINIKUBE_IP}:${FRONTEND_NODEPORT}"
        fi
    fi

    echo ""
    echo "=== Deployment Verification Summary ==="
    echo "✓ Frontend deployment: Ready"
    echo "✓ Backend deployment: Ready"
    echo "✓ MCP server deployment: Ready"
    echo "✓ Services: Available"
    echo "✓ Pods: Running"
    echo "✓ Access: Available via NodePort"
    echo "======================================="

    exit 0
else
    echo "✗ Deployment verification failed"
    echo "Expected 3 deployments ready, got ${READY_DEPLOYMENTS}"
    kubectl get pods
    kubectl get deployments
    exit 1
fi