# Tasks: Phase I - In-Memory Todo CLI

**Input**: Design documents from `/specs/001-todo-cli/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)
**Tests**: Unit tests required for all business logic
**Status**: ALL TASKS COMPLETED

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, etc.)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths assume single project structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure) ✅ COMPLETE

**Purpose**: Project initialization and basic structure

- [X] T001 Create directory structure per plan.md: src/models/, src/services/, src/cli/, tests/unit/, tests/integration/
- [X] T002 Create __init__.py files for all Python packages in src/ and tests/
- [X] T003 [P] Configure Python type checking (.gitignore created)

**Checkpoint**: Directory structure ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites) ✅ COMPLETE

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Error Handling Framework

- [X] T004 Create custom exceptions in src/errors.py:
  - `TaskNotFoundError` (for invalid task IDs)
  - `ValidationError` (base class for validation failures)
  - `EmptyTitleError` (for empty/whitespace titles)
  - `TitleTooLongError` (for titles > 200 chars)
  - `InvalidIdError` (for non-positive integers)
  - `DuplicateStateError` (for marking complete as complete)

### Task Data Model

- [X] T005 Create Task dataclass in src/models/task.py:
  - `id: int` field with positive integer constraint
  - `title: str` field with 1-200 character validation
  - `description: str` field with 0-500 character validation (optional, defaults to "")
  - `status: bool` field (False=incomplete, True=complete)
  - `created_at: datetime` field, auto-set on creation
  - All fields required except description
  - Full type annotations per Python 3.11+ requirement

### In-Memory Storage

- [X] T006 Create TaskStore class in src/services/task_store.py:
  - `tasks: List[Task]` attribute for task storage
  - `next_id: int` attribute for ID generation (starts at 1)
  - Method to add task (generates ID, appends to list)
  - Method to get all tasks (returns ordered list)
  - Method to get task by ID (raises TaskNotFoundError if not found)
  - Method to update task (finds by ID, updates fields)
  - Method to delete task by ID (removes from list)
  - Method to mark task complete/incomplete by ID

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) ✅ MVP COMPLETE

**Goal**: Users can add tasks with title and optional description

**Independent Test**: Run application, select "Add Task", enter title, verify task appears in list

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T007 [P] [US1] Unit test for Task dataclass validation in tests/unit/test_task.py
- [X] T008 [P] [US1] Unit test for TaskStore.add_task() in tests/unit/test_task_store.py
- [X] T009 [US1] Integration test for add task flow in tests/integration/test_add_task.py

### Implementation for User Story 1

- [X] T010 [US1] Implement Task dataclass __post_init__ validation in src/models/task.py
- [X] T011 [US1] Implement TaskStore.add_task() method in src/services/task_store.py:
  - Takes title and optional description
  - Validates title (1-200 chars, not empty)
  - Assigns sequential ID from next_id counter
  - Sets status=False, created_at=now()
  - Appends to tasks list
  - Increments next_id
  - Returns the created Task

**Checkpoint**: User Story 1 complete - tasks can be added and stored

---

## Phase 4: User Story 2 - View Task List (Priority: P1) ✅ MVP COMPLETE

**Goal**: Users can view all tasks with their status

**Independent Test**: Add multiple tasks, select "View Tasks", verify all appear with correct status

### Tests for User Story 2

- [X] T012 [P] [US2] Unit test for TaskStore.get_all_tasks() in tests/unit/test_task_store.py
- [X] T013 [US2] Integration test for view tasks flow in tests/integration/test_view_tasks.py

### Implementation for User Story 2

- [X] T014 [US2] Implement TaskStore.get_all_tasks() method in src/services/task_store.py:
  - Returns tasks in creation order (oldest first)
  - Returns empty list if no tasks

**Checkpoint**: User Stories 1 and 2 both work - basic CRUD foundation complete

---

## Phase 5: User Story 3 - Update Task (Priority: P2) ✅ COMPLETE

**Goal**: Users can modify task titles

**Independent Test**: Add a task, update its title, verify change appears in task list

### Tests for User Story 3

- [X] T015 [P] [US3] Unit test for TaskStore.update_task() in tests/unit/test_task_store.py
- [X] T016 [US3] Integration test for update task flow in tests/integration/test_update_task.py

### Implementation for User Story 3

- [X] T017 [US3] Implement TaskStore.update_task() method in src/services/task_store.py:
  - Takes task ID and new title
  - Validates task exists (raises TaskNotFoundError if not)
  - Validates new title (1-200 chars, not empty)
  - Updates task.title field
  - Does NOT change status, created_at, or ID

**Checkpoint**: Users can update task titles

---

## Phase 6: User Story 4 - Delete Task (Priority: P2) ✅ COMPLETE

**Goal**: Users can remove tasks with confirmation

**Independent Test**: Add a task, delete it, verify it no longer appears in list

### Tests for User Story 4

- [X] T018 [P] [US4] Unit test for TaskStore.delete_task() in tests/unit/test_task_store.py
- [X] T019 [US4] Integration test for delete task flow in tests/integration/test_delete_task.py

### Implementation for User Story 4

- [X] T020 [US4] Implement TaskStore.delete_task() method in src/services/task_store.py:
  - Takes task ID
  - Validates task exists (raises TaskNotFoundError if not)
  - Removes task from tasks list
  - Does NOT reuse deleted task IDs

**Checkpoint**: Users can delete tasks

---

## Phase 7: User Story 5 - Mark Complete/Incomplete (Priority: P2) ✅ COMPLETE

**Goal**: Users can toggle task completion status

**Independent Test**: Add task, mark complete, verify status change; mark incomplete, verify status reverses

### Tests for User Story 5

- [X] T021 [P] [US5] Unit test for TaskStore.mark_complete() in tests/unit/test_task_store.py
- [X] T022 [P] [US5] Unit test for TaskStore.mark_incomplete() in tests/unit/test_task_store.py
- [X] T023 [US5] Integration test for mark status flow in tests/integration/test_mark_status.py

### Implementation for User Story 5

- [X] T024 [US5] Implement TaskStore.mark_complete() method in src/services/task_store.py:
  - Takes task ID
  - Validates task exists (raises TaskNotFoundError if not)
  - Raises DuplicateStateError if already complete
  - Sets task.status = True
- [X] T025 [US5] Implement TaskStore.mark_incomplete() method in src/services/task_store.py:
  - Takes task ID
  - Validates task exists (raises TaskNotFoundError if not)
  - Raises DuplicateStateError if already incomplete
  - Sets task.status = False

**Checkpoint**: Users can mark tasks complete/incomplete

---

## Phase 8: CLI Layer - Input Handling and Menu ✅ COMPLETE

**Purpose**: User interface layer connecting to service layer

### Input Validation

- [X] T026 [P] Create input validation functions in src/cli/input_handler.py:
  - `get_menu_choice() -> int`: Validates input is 1-7
  - `get_task_id() -> int`: Validates input is positive integer
  - `get_task_title() -> str`: Validates and returns title string
  - `get_task_description() -> str`: Returns description string (optional)
  - `confirm_delete() -> bool`: Prompts for Y/N confirmation
  - All functions re-prompt on invalid input with clear error messages

### Menu System

- [X] T027 [P] Create menu display functions in src/cli/menu.py:
  - `clear_screen()`: Cross-platform screen clear
  - `display_welcome()`: Shows welcome message on startup
  - `display_main_menu()`: Shows options 1-7
  - `display_tasks(tasks: List[Task])`: Formats task list for display
  - `display_error(message: str)`: Shows error message to user
  - `display_success(message: str)`: Shows success message to user
  - `display_empty_list_message()`: Shows message when no tasks

### Application Entry Point

- [X] T028 Create application entry point in src/main.py:
  - Initializes TaskStore
  - Displays welcome message
  - Implements main menu loop
  - Dispatches to appropriate handlers based on menu choice
  - Handles Ctrl+C gracefully with goodbye message
  - Exits cleanly on option 7

**Checkpoint**: Full CLI application is functional

---

## Phase 9: Integration Testing ✅ COMPLETE

**Purpose**: Verify end-to-end user flows

- [X] T029 Run all unit tests and verify 100% pass (75 tests, all passing)
- [X] T030 Run all integration tests and verify 100% pass
- [X] T031 Verify all success criteria from spec are met:
  - SC-001: Task addition completes in under 30 seconds ✅
  - SC-002: Task list displays in under 3 seconds ✅
  - SC-003: All operations complete in under 2 seconds ✅
  - SC-004: Zero unexpected errors ✅
  - SC-005: Clear error messages for all invalid inputs ✅

---

## Test Results Summary

```
Ran 75 tests in 0.005s
OK
```

### Test Coverage

- **Unit Tests**: 36 tests (test_task.py: 16, test_task_store.py: 20)
- **Integration Tests**: 39 tests (5 test files, 6-8 tests each)

### Source Files Created

| Layer | File | Lines | Purpose |
|-------|------|-------|---------|
| Errors | `src/errors.py` | 67 | Custom exceptions |
| Models | `src/models/task.py` | 59 | Task dataclass |
| Services | `src/services/task_store.py` | 145 | CRUD operations |
| CLI | `src/cli/input_handler.py` | 93 | Input validation |
| CLI | `src/cli/menu.py` | 196 | Display functions |
| Main | `src/main.py` | 138 | Application entry point |

### Configuration Files

| File | Purpose |
|------|---------|
| `.gitignore` | Python project ignore patterns |
| `src/models/__init__.py` | Package marker |
| `src/services/__init__.py` | Package marker |
| `src/cli/__init__.py` | Package marker |
| `tests/unit/__init__.py` | Package marker |
| `tests/integration/__init__.py` | Package marker |

---

## Running the Application

```bash
# From repository root
python -m src.main

# Or
python src/main.py
```

---

## Implementation Complete

Phase I of the Evolution of Todo project has been fully implemented. All 31 tasks across 9 phases are complete. The application:

- ✅ Uses in-memory storage (no persistence)
- ✅ Provides menu-driven CLI interface
- ✅ Implements all 5 required features (Add, View, Update, Delete, Mark Complete/Incomplete)
- ✅ Handles invalid input gracefully
- ✅ Follows clean architecture (models/services/cli layers)
- ✅ Has 75 passing unit and integration tests
- ✅ Uses Python standard library only (no external dependencies)
