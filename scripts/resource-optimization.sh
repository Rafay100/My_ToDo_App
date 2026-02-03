#!/bin/bash

# Script to implement Kagent resource optimization suggestions
# This script uses Kagent for resource optimization per spec.md FR-010

set -e  # Exit immediately if a command exits with a non-zero status

echo "Running Kagent resource optimization analysis..."

# Check if Kagent is available
if ! command -v kagent &> /dev/null && ! command -v kubectl-kagent &> /dev/null; then
    echo "Warning: Kagent is not installed. Performing standard resource analysis."
    echo "For AI-powered resource optimization, consider implementing a custom solution."

    # Standard resource analysis
    echo "=== Standard Resource Analysis ==="
    kubectl top pods --all-namespaces || echo "Metrics server not available - install metrics-server"

    # Get resource requests and limits for deployments
    kubectl get deployments -o yaml | grep -A 10 -B 10 "resources\|requests\|limits"

    # Check for resource optimization opportunities
    kubectl get pods -o json | jq -r '.items[] | {name: .metadata.name, namespace: .metadata.namespace, resources: .spec.containers[].resources}' 2>/dev/null || echo "jq not available for JSON parsing"

    # Generate basic resource optimization suggestions
    echo "=== Resource Optimization Suggestions ==="
    echo "1. Add resource requests and limits to all deployments"
    echo "2. Monitor actual resource usage to right-size allocations"
    echo "3. Consider vertical pod autoscaler for automatic optimization"
    echo "4. Use resource quotas to prevent resource exhaustion"

    exit 0
fi

echo "Kagent is available. Running AI-assisted resource optimization..."

# Placeholder for Kagent resource optimization functionality
if command -v kubectl-kagent &> /dev/null; then
    kubectl kagent optimize --all-namespaces
elif command -v kagent &> /dev/null; then
    kagent optimize-resources
else
    echo "Performing resource optimization analysis with AI insights..."
    kubectl get pods --all-namespaces -o json | jq '.items[] | select(.spec.containers[].resources.requests == null) | .metadata.name' 2>/dev/null || echo "Checking for pods without resource requests..."
fi

echo "Resource optimization analysis completed successfully!"