# Implementation Plan: Advanced Cloud-Native Todo AI Platform

**Branch**: `1-advanced-cloud-native` | **Date**: 2026-02-04 | **Spec**: [link to spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-advanced-cloud-native/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of Phase V event-driven architecture for the Todo AI Platform, focusing on advanced task features (recurring tasks, due dates, reminders, priorities, tags), event-driven microservices with Kafka messaging, Dapr runtime abstraction, and deployment to both local Minikube and cloud Kubernetes (AKS/GKE/OKE). The system follows an event-driven, microservices architecture as mandated by the constitution.

## Technical Context

**Language/Version**: Python 3.11, TypeScript/JavaScript, Dapr SDKs, Kafka Connectors
**Primary Dependencies**: Dapr (1.12+), Apache Kafka (3.7+), Strimzi/Redpanda, PostgreSQL (Neon), OpenAI SDK, MCP SDK, Kubernetes (1.27+), Helm 3.x
**Storage**: Neon Serverless PostgreSQL (existing in Phase III) with Dapr state management
**Testing**: Integration tests for event-driven flows, end-to-end tests for advanced features
**Target Platform**: Kubernetes (Minikube, AKS, GKE, OKE) with Dapr sidecars
**Project Type**: Event-driven microservices (frontend, backend/MCP, notification, recurring-task, audit services)
**Performance Goals**: Sub-200ms response time for task operations, sub-500ms event processing, 99.9% availability
**Constraints**: Event-driven architecture mandatory, Dapr for all cross-service communication, Kafka for messaging, cloud-native deployment with Helm
**Scale/Scope**: Multi-environment deployment (local Minikube + cloud Kubernetes) with consistent configuration

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ **Phase V Compliance**: Uses Event-driven architecture, Dapr, Kafka, Cloud deployment as required
- ✅ **Architecture**: Event-driven microservices as required by constitution
- ✅ **Technology Matrix**: Uses Dapr, Kafka, Kubernetes, Helm as specified
- ✅ **Deployment Targets**: Supports Minikube (local) and AKS/GKE/OKE (cloud) as required
- ✅ **Dapr Integration**: Full feature set (Pub/Sub, State, Service Invocation, Jobs/Cron, Secrets) as required
- ✅ **Kafka Messaging**: Properly integrated via Dapr Pub/Sub as required
- ✅ **Helm Charts**: Reused from Phase IV as required
- ✅ **Event-driven Architecture**: Mandatory for Phase V as per constitution
- ✅ **Cloud-native Deployment**: Consistent deployment across environments as required
- ✅ **Research Complete**: All technology decisions researched and documented in research.md
- ✅ **Data Model Aligned**: Data model supports all required features as per spec
- ✅ **API Contracts Validated**: API contracts support advanced features and event-driven patterns

## Project Structure

### Documentation (this feature)

```text
specs/1-advanced-cloud-native/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── task.py              # Extended task model with due_date, recurrence, priority, tags
│   │   └── task_template.py     # Recurring task template model
│   ├── services/
│   │   ├── task_service.py      # Task management with advanced features
│   │   ├── notification_service.py # Notification service for reminders
│   │   ├── recurring_task_service.py # Service for generating recurring tasks
│   │   └── audit_service.py     # Audit service for event logging
│   ├── api/
│   │   └── advanced_todo_api.py # Endpoints for advanced features
│   ├── dapr_components/
│   │   ├── pubsub.yaml          # Dapr pub/sub component for Kafka
│   │   ├── statestore.yaml      # Dapr state store component for PostgreSQL
│   │   └── secrets.yaml         # Dapr secrets component
│   └── mcp/
│       └── advanced_tools.py    # MCP tools for advanced features
│
notification-service/
├── src/
│   ├── main.py                  # Notification service entry point
│   ├── consumers/
│   │   └── reminder_consumer.py # Consumer for reminder events
│   └── providers/
│       └── notification_provider.py # Notification delivery mechanisms
│
recurring-task-service/
├── src/
│   ├── main.py                  # Recurring task service entry point
│   ├── generators/
│   │   └── task_generator.py    # Recurring task generation logic
│   └── schedulers/
│       └── cron_scheduler.py    # Cron-based scheduling using Dapr Jobs API
│
audit-service/
├── src/
│   ├── main.py                  # Audit service entry point
│   └── persisters/
│       └── event_persister.py   # Event persistence logic
│
dapr/
├── components/
│   ├── pubsub.yaml              # Kafka pub/sub configuration
│   ├── statestore.yaml          # PostgreSQL state store
│   ├── secrets.yaml             # Secret store configuration
│   └── bindings.yaml            # Input/output bindings
└── configurations/
    └── appconfig.yaml           # Dapr application configuration
│
charts/
├── todo-ai-platform/            # Helm chart for the entire platform
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── templates/
│   │   ├── frontend-deployment.yaml
│   │   ├── frontend-service.yaml
│   │   ├── backend-deployment.yaml
│   │   ├── backend-service.yaml
│   │   ├── notification-service-deployment.yaml
│   │   ├── recurring-task-service-deployment.yaml
│   │   ├── audit-service-deployment.yaml
│   │   ├── kafka-strimzi-crds.yaml
│   │   ├── kafka-cluster.yaml
│   │   ├── kafka-topic-task-events.yaml
│   │   ├── kafka-topic-reminders.yaml
│   │   ├── kafka-topic-task-updates.yaml
│   │   └── _helpers.tpl
│   └── README.md
│
scripts/
├── deploy-local.sh              # Deploy to Minikube with Dapr and Kafka
├── deploy-cloud.sh              # Deploy to cloud Kubernetes
└── validate-deployment.sh       # Validate event-driven functionality
```

**Structure Decision**: Selected event-driven microservices approach with Dapr as the runtime abstraction layer, enabling loose coupling between services while maintaining consistent communication patterns. Kafka provides reliable messaging infrastructure, and the architecture supports both local and cloud deployment with identical configuration.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple service deployments | Event-driven architecture requires separation of concerns for notification, recurring tasks, and audit services | Would create monolithic service difficult to scale and maintain |
| Dapr sidecar injection | Constitution mandates Dapr for all Phase V cross-service communication | Direct service-to-service communication would violate Phase V constraints |
| Kafka integration | Event-driven architecture requires reliable messaging infrastructure | In-memory queues would not provide durability and scalability required |
| Complex deployment configuration | Multi-environment deployment (Minikube + cloud) requires sophisticated configuration management | Simplified configuration would not support consistent deployment across environments |