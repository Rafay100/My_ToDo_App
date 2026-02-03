# Quickstart Guide: Advanced Cloud-Native Todo AI Platform

**Feature**: Advanced Cloud-Native Todo AI Platform
**Date**: 2026-02-04
**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

## Overview

This guide provides a quick introduction to setting up and using the Advanced Cloud-Native Todo AI Platform with event-driven architecture, Dapr runtime abstraction, and Kafka messaging.

## Prerequisites

- Docker Desktop
- Minikube or access to cloud Kubernetes (AKS/GKE/OKE)
- kubectl
- Helm 3.x
- Dapr CLI
- Kafka (Strimzi for local, managed for cloud)

## Local Development Setup

### 1. Install Dapr

```bash
# Download and install Dapr CLI
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash

# Initialize Dapr in your local environment
dapr init
```

### 2. Start Minikube with Dapr

```bash
# Start Minikube
minikube start --driver=docker

# Install Dapr on Minikube
dapr init -k
```

### 3. Deploy Kafka with Strimzi

```bash
# Install Strimzi operator
kubectl create namespace kafka
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

# Wait for the cluster operator to be ready
kubectl wait --for=condition=ready pod -n kafka --selector=name=strimzi-cluster-operator

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
```

### 4. Configure Dapr Components

```bash
# Create Dapr components directory
mkdir -p dapr/components

# Create Kafka pub/sub component
cat <<EOF > dapr/components/pubsub.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092"
  - name: consumerGroup
    value: "dapr-consumer-group"
  - name: authRequired
    value: "false"
EOF

# Create PostgreSQL state store component
cat <<EOF > dapr/components/statestore.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: postgresql-statestore
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    value: "host=neon-postgres user=postgres password=password dbname=todo_db port=5432 sslmode=require"
  - name: tableName
    value: "dapr_state_store"
  - name: migrationTableName
    value: "dapr_state_store_migrations"
  - name: actorStateStore
    value: "true"
EOF

# Deploy Dapr components
kubectl apply -f dapr/components/
```

### 5. Deploy the Platform with Helm

```bash
# Add the charts directory to your Kubernetes cluster
helm install todo-platform charts/todo-ai-platform/ --values charts/todo-ai-platform/values-dev.yaml
```

## Platform Architecture

### Core Services

1. **Frontend Service**: Next.js application for user interaction
2. **Backend Service**: FastAPI application with OpenAI integration
3. **Notification Service**: Handles scheduled reminders and notifications
4. **Recurring Task Service**: Generates recurring task instances based on templates
5. **Audit Service**: Logs all system events for compliance and debugging

### Event Flow

1. User creates/updates task → Event published to `task-events` topic
2. Notification service listens for due dates → Schedules reminders in `reminders` topic
3. Recurring task service monitors templates → Creates new tasks via `task-events`
4. All services publish audit logs to `task-updates` topic

## Key Features

### Advanced Task Management
- Create tasks with due dates, priorities, and tags
- Set recurring tasks with various patterns (daily, weekly, monthly, yearly)
- Schedule reminders for upcoming deadlines

### Event-Driven Architecture
- All task operations trigger events via Kafka
- Services react to events asynchronously
- Loose coupling between platform components

### Dapr Integration
- Service-to-service invocation through Dapr
- State management with PostgreSQL via Dapr
- Secrets management through Dapr
- Pub/Sub messaging via Dapr and Kafka

## API Usage Examples

### Create a Task with Advanced Features

```bash
curl -X POST "http://localhost:3000/api/tasks" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Submit quarterly report",
    "description": "Prepare and submit Q1 financial report",
    "priority": "high",
    "due_date": "2026-03-15T10:00:00Z",
    "tags": ["work", "report", "finance"],
    "recurrence_rule": "FREQ=WEEKLY;INTERVAL=1;COUNT=4"
  }'
```

### Query Tasks with Filters

```bash
curl "http://localhost:3000/api/tasks?priority=high&due_date_from=2026-02-01&sort_by=due_date&sort_order=asc" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Development Workflow

1. **Local Development**: Use Dapr with `dapr run` for local service development
2. **Integration Testing**: Deploy to Minikube for full integration testing
3. **Event Simulation**: Use Kafka tools to simulate event flows
4. **Monitoring**: Use Dapr dashboard and Kafka monitoring tools

## Troubleshooting

### Common Issues

1. **Kafka Connection Issues**: Verify Kafka cluster is running and accessible
2. **Dapr Sidecar Issues**: Check if Dapr sidecars are injected properly
3. **Event Processing Delays**: Monitor Kafka topic lag and consumer group status

### Useful Commands

```bash
# Check Dapr status
dapr status -k

# Monitor Kafka topics
kubectl -n kafka run kafka-consumer -ti --image=quay.io/strimzi/kafka:latest-kafka-3.7.0 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic task-events --from-beginning

# View platform logs
kubectl logs -l app=todo-platform -f
```

## Next Steps

- Explore the API documentation at `/api/docs`
- Review the data models in `data-model.md`
- Check the complete deployment guides in the repository
- Look at the contract specifications in `contracts/`