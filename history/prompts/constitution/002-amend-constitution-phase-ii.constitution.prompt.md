---
id: "002"
title: "Amend constitution Phase II technology matrix"
stage: "constitution"
date: "2025-12-30"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "project_owner"
command: "/sp.constitution"
labels: ["constitution","governance","technology-matrix","phase-ii"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - ".specify/memory/constitution.md"
  - ".specify/templates/plan-template.md"
  - ".specify/templates/spec-template.md"
  - ".specify/templates/tasks-template.md"
tests:
  - "null"
---

## Prompt

Amend the global constitution technology matrix to reflect Phase II requirements as follows:

Phase II:
- Backend: Python REST API
- Database: Neon Serverless PostgreSQL
- ORM/Data layer: SQLModel or equivalent
- Frontend: Next.js (React, TypeScript)
- Authentication: Better Auth (signup/signin)
- Architecture: Full-stack web application

Phase I remains:
- In-memory console application only

Phase III and later:
- Advanced cloud infrastructure, agents, AI, orchestration

Rules:
- Authentication is allowed starting Phase II
- Web frontend is allowed starting Phase II
- Neon PostgreSQL is allowed starting Phase II
- No AI or agent frameworks until later phases

This amendment must preserve phase isolation and act as the authoritative technology policy.

## Response snapshot

Amended constitution to v1.1.0 and updated dependent templates:
- Updated `.specify/memory/constitution.md` with the new Phase II technology matrix and governance rules.
- Explicitly allowed Better Auth, Next.js, and Neon PostgreSQL for Phase II.
- Prohibited AI/agent frameworks until Phase III+.
- Updated `.specify/templates/plan-template.md`, `spec-template.md`, and `tasks-template.md` to reflect these changes in examples and structural placeholders.

## Outcome

- ✅ Impact: Phase II technology stack solidified and isolated from Phase I and Phase III.
- 📁 Files: constitution.md, plan-template.md, spec-template.md, tasks-template.md
- 🔁 Next prompts: Phase II feature design or Phase I implementation.
- 🧠 Reflection: Strengthening phase boundaries reduces architectural leakage and simplifies early development.

## Evaluation notes (flywheel)

- Failure modes observed: "null"
- Graders run and results (PASS/FAIL): "null"
- Prompt variant (if applicable): "null"
- Next experiment (smallest change to try): "null"
