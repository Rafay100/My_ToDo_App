---
id: 2
title: "Fix signup path and CORS configuration"
stage: "misc"
date_iso: "2026-01-01"
surface: "agent"
model: "claude-sonnet-4.5"
feature: "fullstack-todo-app"
branch: "002-fullstack-todo-app"
user: "SYED RAFAY"
command: "Fix signup path and CORS mismatch"
labels: ["cors", "api-path", "fastapi", "nextjs"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml:
  - backend/src/main.py
  - frontend/src/services/auth_client.ts
tests_yaml:
  - Verify POST /api/v1/signup works in Swagger
  - Verify Frontend calls port 8000
---

## Prompt History Record

### PROMPT_TEXT
I have a working FastAPI backend and a Next.js frontend, but signup shows “Failed to fetch”.

FACTS (do not assume anything else):
- Frontend runs on: http://localhost:3001
- Backend runs on: http://localhost:8000
- FastAPI Swagger shows these routes ONLY:
  POST /api/v1/signup
  POST /api/v1/signin
  POST /api/v1/signout
- /signup or /auth/signup do NOT exist
- Backend works correctly in Swagger UI

YOUR TASK (must follow in order):

1. Identify why “Failed to fetch” happens when frontend calls the wrong API path.
   Use Fetch API specifications, not opinions.

2. Locate the frontend signup request (fetch or axios) and FIX IT so it calls:
   http://localhost:8000/api/v1/signup
   (include full corrected code snippet).

3. Ensure headers and body are correct JSON:
   Content-Type: application/json

4. Verify and fix CORS in FastAPI so it allows:
   http://localhost:3001
   (show exact CORSMiddleware configuration).

5. Explain why relative URLs (like /signup) break when frontend and backend run on different ports.

6. Give a final 5-step checklist

### RESPONSE_TEXT
The assistant identified that relative paths resolve to the frontend origin, causing connection failures for POST requests. It provided the corrected `signupUser` service code using the absolute URL `http://localhost:8000/api/v1/signup` and JSON headers. It also provided the exact FastAPI CORS configuration to allow `http://localhost:3001` and explained the security constraints of different origins (ports). A 5-step verification checklist was provided.
