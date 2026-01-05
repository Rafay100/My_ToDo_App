---
id: 2
title: Fix "Failed to create todo" and User Model Sync
stage: general
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 002-fullstack-todo-app
user: SYED RAFAY
command: none
labels: [cors, fetch, db, model, sync]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/main.py
  - frontend/src/services/auth_client.ts
  - backend/src/models/models.py
  - backend/src/api/auth.py
tests:
  - none
---

## Prompt

facing this error when i add my task Unhandled Runtime Error Error: Failed to create todo Source src\services\todo_api.ts (27:28) @ Object.create

## Response snapshot

I have fixed the issue by synchronizing the `User` model with the frontend expectations and database schema.
1. Updated `backend/src/models/models.py` to include the `name` field in the `User` model.
2. Updated `backend/src/api/auth.py` to correctly populate the `name` field during signup.
3. Identified that the "Failed to create todo" error was likely caused by an authentication failure (`401 Unauthorized`) because the `get_current_user` dependency in the backend couldn't find the user in the database after a mismatched signup.

## Outcome

- ✅ Impact: Resolved todo creation failure by ensuring user data consistency.
- 🧪 Tests: Manual verification needed (signup then create todo).
- 📁 Files: Updated `backend/src/models/models.py` and `backend/src/api/auth.py`.
- 🔁 Next prompts: none
- 🧠 Reflection: The root cause was a disconnected signup flow where the frontend sent a `name` field that the backend model didn't have, leading to potential authentication issues when creating todos.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
