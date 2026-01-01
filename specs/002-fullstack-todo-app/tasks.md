# Tasks: Phase II Full-Stack Todo App

**Input**: Design documents from `/specs/002-fullstack-todo-app/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/todos-api.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 [P] Initialize backend directory with FastAPI/SQLModel dependencies in backend/
- [ ] T002 [P] Initialize frontend directory with Next.js 14+ (App Router) dependencies in frontend/
- [ ] T003 [P] Configure backend linting and formatters in backend/
- [ ] T004 [P] Configure frontend linting and formatters in frontend/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure and database setup

- [x] T005 [P] Setup Neon PostgreSQL connection logic in backend/src/db.py
- [x] T006 [P] Implement User model in backend/src/models/user.py
- [x] T007 [P] Implement Todo model in backend/src/models/todo.py
- [x] T008 Setup Alembic migrations and create initial schema in backend/alembic/
- [x] T009 [P] Initialize Better Auth configuration in frontend/src/lib/auth.ts
- [x] T010 Implement backend authentication middleware to verify session tokens in backend/src/api/auth_middleware.py

**Checkpoint**: Foundation ready - User stories can now begin

---

## Phase 3: User Story 1 - Secure Account Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to sign up and sign in securely

**Independent Test**: Register a user, log out, and log back in

- [x] T011 [US1] Create signup page UI in frontend/src/app/(auth)/signup/page.tsx
- [x] T012 [US1] Create signin page UI in frontend/src/app/(auth)/signin/page.tsx
- [x] T013 [US1] Integrate Better Auth signup/signin logic in frontend/src/services/auth_client.ts
- [x] T014 [US1] Implement user session state provider in frontend/src/components/auth-provider.tsx

**Checkpoint**: User Story 1 (Auth) complete and testable

---

## Phase 4: User Story 2 - Personal Todo Persistence (Priority: P1) 🎯 MVP

**Goal**: CRUD todos with persistent database storage and user isolation

**Independent Test**: Create a todo, refresh page, verify it persists and is private

- [x] T015 [P] [US2] Implement GET /todos API endpoint in backend/src/api/todos.py
- [x] T016 [P] [US2] Implement POST /todos API endpoint in backend/src/api/todos.py
- [x] T017 [P] [US2] Implement DELETE /todos/{id} API endpoint in backend/src/api/todos.py
- [x] T018 [US2] Enforce user-scoped data access for all todo endpoints in backend/src/api/todos.py
- [x] T019 [US2] Create todo list dashboard UI in frontend/src/app/dashboard/page.tsx
- [x] T020 [US2] Implement API client for todo CRUD operations in frontend/src/services/todo_api.ts
- [x] T021 [US2] Add "Add Todo" and "Delete Todo" interactions in frontend/src/app/dashboard/page.tsx

**Checkpoint**: User Story 2 (Persistence) complete and testable

---

## Phase 5: User Story 3 - Task Lifecycle Management (Priority: P2)

**Goal**: Update todo content and completion status

**Independent Test**: Toggle completion and edit text, verify changes persist

- [x] T022 [P] [US3] Implement PATCH /todos/{id} API endpoint in backend/src/api/todos.py
- [x] T023 [US3] Add completion toggle UI interaction in frontend/src/app/dashboard/todo-item.tsx
- [x] T024 [US3] Add inline edit UI interaction for todo titles in frontend/src/app/dashboard/todo-item.tsx

**Checkpoint**: User Story 3 (Lifecycle) complete and testable

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final refinements and error handling

- [x] T025 [P] Implement global backend error handler in backend/src/main.py
- [x] T026 [P] Add responsive CSS for mobile/desktop viewports in frontend/src/app/globals.css
- [x] T027 [P] Implement frontend error boundaries and empty state UIs in frontend/src/components/
- [x] T028 [P] Update project README with finalized Quickstart instructions

---

## Dependencies & Execution Order

### Phase Dependencies
- **Phase 1 (Setup)**: Start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1
- **Phase 3 & 4 (US1 & US2)**: Depend on Phase 2. Can run in parallel once foundation is ready.
- **Phase 5 (US3)**: Depends on Phase 4 foundation.

### Parallel Opportunities
- Backend and Frontend setup (T001, T002)
- User and Todo model definitions (T006, T007)
- API endpoint implementations (T015, T016, T017, T022)
- Frontend UI development across different auth pages (T011, T012)
