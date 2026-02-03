<!--
  SYNC IMPACT REPORT
  Version change: 1.1.0 -> 1.2.0
  List of modified principles:
    - IV. Technology Constraints (Updated Phase III matrix and rules)
  Added sections:
    - Phase III specific technologies (OpenAI ChatKit, OpenAI Agents SDK, MCP SDK)
    - Phase III architecture rules (Stateless AI-driven system, MCP tools)
    - Phase III constraints (No server-side session memory, no background workers, etc.)
  Removed sections:
    - Vague "Advanced cloud infrastructure" and "Distributed systems" from Phase III
  Templates requiring updates:
    - .specify/templates/plan-template.md (✅ updated)
    - .specify/templates/spec-template.md (✅ updated)
    - .specify/templates/tasks-template.md (✅ updated)
  Follow-up TODOs: None
-->

# Evolution of Todo Constitution

## Core Principles

### I. Spec-Driven Development (MANDATORY)

Every feature MUST originate from an approved specification. No agent may write code without:
- An approved spec.md defining requirements and user stories
- An approved plan.md defining architecture and interfaces
- An approved tasks.md defining implementation steps

The mandatory workflow sequence is:
1. Constitution (this document) - governing principles
2. Specs (`/specs/[feature]/spec.md`) - requirements and user stories
3. Plan (`/specs/[feature]/plan.md`) - architecture decisions
4. Tasks (`/specs/[feature]/tasks.md`) - implementation checklist
5. Implement (`/sp.implement`) - code execution

Deviation from this sequence is prohibited. Refinements MUST occur at the spec level, not during implementation.

**Rationale**: Prevents scope creep, ensures alignment, and enables verifiable progress.

### II. Agent Behavior Rules

All agents MUST adhere to the following constraints:

- **No manual coding by humans**: Agents execute all code changes. Humans provide intent, not implementation.
- **No feature invention**: Agents MUST NOT add functionality not specified in approved specs and tasks.
- **No deviation from approved specifications**: Implementation must match the approved spec exactly.
- **Refinement at spec level**: If implementation reveals gaps, the spec MUST be updated before proceeding.

Agents MUST surface ambiguity rather than make assumptions. When requirements are unclear, agents MUST ask clarifying questions before proceeding.

**Rationale**: Ensures predictable outcomes and maintains architectural coherence.

### III. Phase Governance

Each phase is strictly scoped by its specification:

- **Phase I**: In-memory console application ONLY.
- **Phase II**: Full-stack web application (Next.js, Python REST API, Neon PostgreSQL).
- **Phase III**: AI-powered todo chatbot with OpenAI Agents SDK, MCP tools, and stateless architecture.

Features defined in Phase N specifications MUST NOT include capabilities planned for Phase N+1 or later.
Authentication, Web Frontend, and Neon PostgreSQL are EXPLICITLY ALLOWED starting Phase II.
No AI or agent frameworks are allowed until Phase III or later.

**Rationale**: Maintains project discipline and enables incremental value delivery through strictly isolated phases.

### IV. Technology Constraints

All code MUST adhere to the following technology matrix:

**Phase I (Legacy/Current foundation)**:
- In-memory data storage
- Console-based interaction

**Phase II (Target)**:
- **Backend**: Python REST API (FastAPI)
- **Database**: Neon Serverless PostgreSQL
- **ORM/Data layer**: SQLModel or equivalent
- **Frontend**: Next.js (React, TypeScript)
- **Authentication**: Better Auth (signup/signin)
- **Architecture**: Full-stack web application
- **API Style**: REST APIs
- **Constraints**: No AI or agents

**Phase III (Advanced)**:
- **Frontend**: OpenAI ChatKit
- **Backend**: Python FastAPI
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK
- **ORM/Data Layer**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth
- **Architecture**: Stateless AI-driven system using MCP tools
- **Rules**:
  - AI agents are allowed starting Phase III
  - MCP (Model Context Protocol) is allowed starting Phase III
  - Stateless server architecture is required in Phase III
  - All AI state must be persisted in the database
  - No server-side session memory
  - No background workers
  - No real-time streaming
  - No future phase orchestration or infrastructure

Technology choices are fixed for the project duration. Introducing new technologies requires constitutional amendment.

**Rationale**: Reduces cognitive load and ensures consistent architectural patterns while preserving strict phase isolation.

### V. Clean Architecture

All code MUST follow clean architecture principles:

- Clear separation of concerns (models, services, API, UI)
- Dependency inversion - inner layers cannot depend on outer layers
- Business logic independent of frameworks, databases, and delivery mechanisms
- Each component MUST be independently testable

**Rationale**: Enables long-term maintainability and facilitates future refactoring.

### VI. Cloud-Native Readiness

Services MUST be designed for cloud-native deployment:

- **Stateless services where required**: State MUST be externalized to database or cache.
- **12-Factor App compliance**: Configuration via environment, logs to stdout, etc.
- **Observability built-in**: Structured logging, metrics endpoints, and tracing support.
- **Graceful degradation**: Services MUST handle downstream failures elegantly.

**Rationale**: Ensures smooth deployment to modern cloud platforms and enables horizontal scaling.

## Quality Standards

### Code Quality

- All code MUST pass linting and formatting checks
- Type annotations REQUIRED for all Python/TypeScript code
- Docstrings REQUIRED for public APIs and complex functions
- No hardcoded secrets or credentials - use environment variables

### Testing Requirements

- Unit tests for all business logic
- Integration tests for service interactions
- Contract tests for API endpoints
- Tests MUST fail before implementation (Red-Green-Refactor)

### Security Standards

- Authentication and authorization for all protected operations (Phase II+)
- Input validation at all system boundaries
- Audit logging for security-relevant events
- No secrets in source control

## Development Workflow

### Phase 0: Research & Design
- Explore existing codebase and dependencies
- Define technical approach in plan.md
- Identify interfaces and contracts

### Phase 1: Specification
- Create user stories with acceptance criteria
- Define functional requirements
- Establish success metrics

### Phase 2: Planning
- Make architectural decisions in plan.md
- Define project structure (preserving phase separation)
- Document complexity justifications

### Phase 3: Task Breakdown
- Generate tasks.md from plan and spec
- Organize by user story
- Identify dependencies and parallel opportunities

### Phase 4: Implementation
- Execute tasks in dependency order
- Write tests first, ensure they fail
- Implement to match spec exactly

### Phase 5: Validation
- Verify all acceptance criteria met
- Run full test suite
- Update documentation

## Governance

This constitution is the supreme governing document for all agents. It supersedes all other practices, conventions, and informal agreements.

### Amendment Procedure

Amendments to this constitution require:
1. Documentation of the proposed change
2. Rationale explaining the need
3. Impact assessment on existing work
4. Approval from project authority

### Versioning

Constitution versions follow semantic versioning:
- **MAJOR**: Backward-incompatible governance changes
- **MINOR**: New principles or materially expanded guidance
- **PATCH**: Clarifications, wording fixes, typo corrections

### Compliance Review

All work MUST be reviewed against this constitution:
- Plan reviews MUST verify phase scope compliance
- Code reviews MUST verify architecture principles
- Task acceptance MUST verify spec alignment

**Version**: 1.2.0 | **Ratified**: 2025-12-29 | **Last Amended**: 2026-01-20
