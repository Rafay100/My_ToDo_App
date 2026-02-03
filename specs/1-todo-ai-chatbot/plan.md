# Implementation Plan: Todo AI Chatbot

**Branch**: `1-todo-ai-chatbot` | **Date**: 2026-02-03 | **Spec**: [link to spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-todo-ai-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a stateless AI-powered todo chatbot that allows users to manage their tasks through natural language using OpenAI Agents SDK and MCP tools. The system follows a stateless architecture with all data persisted in Neon Serverless PostgreSQL using SQLModel ORM, and provides a conversational UI via OpenAI ChatKit.

## Technical Context

**Language/Version**: Python 3.11, TypeScript for frontend
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, Official MCP SDK, SQLModel, Neon Serverless PostgreSQL, OpenAI ChatKit
**Storage**: Neon Serverless PostgreSQL with SQLModel ORM
**Testing**: pytest for backend, Jest for frontend
**Target Platform**: Web application
**Project Type**: Web (frontend + backend)
**Performance Goals**: Handle 100 concurrent users, response time under 5 seconds
**Constraints**: <200ms p95 for database operations, stateless architecture, no in-memory session state
**Scale/Scope**: Support 10k users, 1M+ tasks

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ **Phase III Compliance**: Uses OpenAI ChatKit (frontend), Python FastAPI (backend), OpenAI Agents SDK, Official MCP SDK
- ✅ **Stateless Architecture**: No in-memory session state, all state persisted to database
- ✅ **Technology Matrix**: Uses SQLModel ORM with Neon Serverless PostgreSQL as required
- ✅ **AI Framework**: Uses OpenAI Agents SDK as specified in Phase III
- ✅ **MCP Server**: Uses Official MCP SDK as required
- ✅ **No Background Workers**: Stateless design with no background processes
- ✅ **No Real-time Streaming**: Request-response model without streaming

## Project Structure

### Documentation (this feature)

```text
specs/1-todo-ai-chatbot/
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
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── conversation.py
│   │   └── message.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py
│   │   ├── mcp_server.py
│   │   ├── database_service.py
│   │   └── todo_operations.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── chat_endpoint.py
│   └── main.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── requirements.txt

frontend/
├── src/
│   ├── components/
│   │   ├── ChatInterface.tsx
│   │   └── MessageList.tsx
│   ├── services/
│   │   └── apiClient.ts
│   ├── pages/
│   │   └── ChatPage.tsx
│   └── types/
│       └── index.ts
├── package.json
└── tsconfig.json
```

**Structure Decision**: Selected Option 2: Web application structure to accommodate both frontend (ChatKit) and backend (FastAPI) components as required by the specification.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple service layers | Separation of concerns for AI, MCP, and database operations | Would create tightly coupled code difficult to test and maintain |