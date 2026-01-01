# Research: Phase II Technical Plan

**Feature**: 002-fullstack-todo-app
**Date**: 2025-12-30

## Decisions and Rationale

### 1. Backend Architecture
- **Decision**: FastAPI with SQLModel and Better Auth integration via custom middleware or dependency.
- **Rationale**: FastAPI provides high-performance asynchronous REST endpoints. SQLModel unifies Pydantic and SQLAlchemy, aligning with the Constitution for type safety and clean models.
- **Alternatives Considered**: Flask (rejected for being less modern/performant), Django (rejected as too heavy for this micro-scoped phase).

### 2. Frontend Architecture
- **Decision**: Next.js App Router with React Server Components (RSC) and Client Components for interactivity.
- **Rationale**: Next.js is the Constitutional standard. App Router simplifies routing and data fetching.
- **Alternatives Considered**: Vite + React (rejected for being a Constitutional deviation and lacking built-in routing/SSR).

### 3. Database Management
- **Decision**: Neon Serverless PostgreSQL with Alembic for migrations (via SQLModel).
- **Rationale**: Neon provides serverless scalability. Alembic is the standard for Python-based schema migrations.

### 4. Authentication Flow
- **Decision**: Better Auth on the frontend with session tokens passed to the FastAPI backend.
- **Rationale**: Better Auth is chosen for its simplicity and Next.js friendliness. The backend will verify session tokens using a shared secret or a session verification endpoint provided by the auth service.

## Research Findings

- **Better Auth Integration**: Better Auth stores sessions in the database. The FastAPI backend can query the same Neon DB to verify sessions, ensuring strict data isolation without complex external JWT validation.
- **SQLModel Identity Map**: SQLModel handles relationships efficiently. A `User` will have a relationship to `Todo` items, enforcing `user_id` checks at the ORM level.
- **Next.js & API**: Frontend will use a dedicated `lib/api.ts` for fetch-based interaction with the backend, handling auth headers automatically.
