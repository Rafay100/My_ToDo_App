# Implementation Plan: Phase I - In-Memory Todo CLI

**Branch**: `001-todo-cli` | **Date**: 2025-12-29 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-todo-cli/spec.md`

## Summary

A Python 3.11+ console application providing a menu-driven interface for managing todo tasks in memory. The application implements CRUD operations (Create, Read, Update, Delete) with task completion status tracking. Architecture follows clean separation of concerns with distinct layers for data models, business logic services, and CLI presentation.

## Technical Context

**Language/Version**: Python 3.11+ (standard library only, no external dependencies required)
**Primary Dependencies**: None (uses Python standard library only)
**Storage**: In-memory Python list (no persistence)
**Testing**: pytest (standard library unittest as fallback)
**Target Platform**: Cross-platform terminal (Linux, macOS, Windows)
**Project Type**: Single console application
**Performance Goals**: All operations complete in under 2 seconds
**Constraints**: No external dependencies, single-file or minimal structure
**Scale/Scope**: Single user, maximum 1000 tasks in memory

## Constitution Check

*GATE: Must pass before proceeding with design.*

- [x] **I. Spec-Driven Development**: Plan derived strictly from approved spec.md
- [x] **II. Agent Behavior Rules**: No new features introduced; only implementation approach described
- [x] **III. Phase Governance**: Phase I scope only; no future-phase concepts included
- [x] **IV. Technology Constraints**: Python standard library; no external dependencies
- [x] **V. Clean Architecture**: Separation of concerns (models, services, CLI) planned
- [x] **VI. Cloud-Native Readiness**: Stateless design; state ephemeral to session

**Result**: All gates PASS. No complexity tracking required.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-cli/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (N/A - no clarifications needed)
├── data-model.md        # Phase 1 output (included below)
├── quickstart.md        # Phase 1 output (included below)
├── contracts/           # Phase 1 output (N/A - no API contracts for CLI app)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models/
│   └── task.py          # Task dataclass with validation
├── services/
│   └── task_service.py  # Business logic (CRUD operations)
├── cli/
│   ├── __init__.py
│   ├── menu.py          # Menu display and navigation
│   └── input_handler.py # User input validation
├── errors.py            # Custom exceptions
└── main.py              # Application entry point

tests/
├── unit/
│   ├── test_task.py
│   └── test_task_service.py
└── integration/
    └── test_cli_flow.py
```

**Structure Decision**: Single project with clean architecture layers (models, services, cli). This enables testability and future extensibility while remaining simple for Phase I.

## Phase 0: Research

No research required. All technical decisions are straightforward based on Python standard library capabilities:
- No external dependencies needed
- No clarifications required
- Standard patterns for console input/output

## Phase 1: Design & Contracts

### Data Model

See `data-model.md` section below.

### Contracts

Not applicable. This is a CLI application with no external API contracts.

---

# Data Model: Task Entity

## Task Structure

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | int | Positive integer, sequential | Unique identifier starting at 1 |
| `title` | str | 1-200 characters, required | Task description |
| `description` | str | 0-500 characters, optional | Extended task details |
| `status` | bool | true=complete, false=incomplete | Completion tracking |
| `created_at` | datetime | Auto-set on creation | Creation timestamp |

## Validation Rules

- **Title**: Must be non-empty string, trimmed length 1-200 characters
- **Description**: Optional, trimmed length 0-500 characters
- **ID**: Must exist in task list for read/update/delete operations
- **Status**: Boolean only; toggles between True and False

## In-Memory Storage Design

```
tasks: List[Task]  # Ordered by creation time, oldest first
next_id: int       # Counter for next sequential ID (starts at 1)
```

## Relationships

- No foreign key relationships (Phase I scope)
- Tasks are independent entities
- Display order based on `created_at` timestamp

---

# Quickstart Guide

## Running the Application

```bash
# From repository root
python -m src.main

# Or with python src/main.py
```

## User Menu Options

```
1. Add Task       - Create a new task
2. View Tasks     - Display all tasks
3. Update Task    - Edit task title
4. Delete Task    - Remove a task
5. Mark Complete  - Mark task as done
6. Mark Incomplete - Reopen a task
7. Exit           - Close application
```

## First-Time Usage

1. Run `python -m src.main`
2. Select option 1 to add your first task
3. Select option 2 to view your task list
4. Use options 3-6 to manage tasks
5. Select option 7 to exit (tasks are not saved)

## Exit Behavior

- Application exits gracefully on option 7 or Ctrl+C
- Tasks are NOT persisted; they exist only during the session
- No configuration files or data files are created

---

## Technical Design Details

### 1. Application Structure

The application follows a layered architecture:

```
┌─────────────────────────────────────┐
│            CLI Layer                │
│  (menu.py, input_handler.py)        │
│  - User interaction                 │
│  - Input/Output handling            │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│           Service Layer             │
│        (task_service.py)            │
│  - Business logic                   │
│  - CRUD operations                  │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│           Model Layer               │
│            (task.py)                │
│  - Data structure                   │
│  - Validation logic                 │
└─────────────────────────────────────┘
```

### 2. In-Memory Data Storage

```python
# Global state (single session only)
class TaskStore:
    tasks: List[Task] = []
    next_id: int = 1
```

The `TaskStore` class encapsulates all in-memory state. It is instantiated once per session and discarded on exit.

### 3. Task Identification Strategy

- **Sequential IDs**: IDs start at 1 and increment by 1 for each new task
- **ID stability**: Once assigned, an ID never changes during the session
- **Deletion behavior**: Deleted tasks are removed; remaining IDs stay unchanged
- **No reuse**: Deleted task IDs are not reused (prevents confusion)

### 4. CLI Control Flow

```
main()
    ├─ Initialize TaskStore
    ├─ Display welcome message
    └─ Menu loop:
        ├─ Display menu options
        ├─ Get user input
        ├─ Validate input (1-7)
        ├─ Dispatch to appropriate handler
        └─ Continue until exit (7)
```

**Input Handling**:
- `input()` for all user input
- Strip whitespace, handle empty input gracefully
- Non-numeric input shows error and redisplays menu
- Ctrl+C triggers graceful exit with goodbye message

**Screen Management**:
- Clear screen between menu displays using `os.system('cls' if os.name == 'nt' else 'clear')`
- Welcome message on first display only

### 5. Separation of Responsibilities

| Layer | File | Responsibility |
|-------|------|----------------|
| Model | `models/task.py` | Task data structure, field validation |
| Service | `services/task_service.py` | CRUD logic, ID management, error raising |
| CLI | `cli/menu.py` | Menu display, user interaction flow |
| CLI | `cli/input_handler.py` | Input parsing, validation, re-prompt on error |
| Errors | `errors.py` | Custom exception classes |

### 6. Error Handling Strategy

**Custom Exceptions**:

```python
class TaskNotFoundError(Exception):
    """Raised when task ID does not exist"""

class ValidationError(Exception):
    """Raised when input fails validation"""

class EmptyTitleError(ValidationError):
    """Raised when title is empty or whitespace"""

class TitleTooLongError(ValidationError):
    """Raised when title exceeds 200 characters"""

class InvalidIdError(ValidationError):
    """Raised when ID is not a positive integer"""
```

**Error Handling Flow**:

1. **Input Validation Errors** (Empty title, invalid ID format):
   - Display user-friendly error message
   - Return to previous menu (no state change)
   - Allow retry without losing context

2. **Task Not Found Error**:
   - Display error with ID that was attempted
   - Return to previous menu
   - No state change

3. **Duplicate Operation Error** (marking complete as complete):
   - Inform user task is already in desired state
   - Return to previous menu

4. **Keyboard Interrupt (Ctrl+C)**:
   - Catch signal
   - Display goodbye message
   - Exit cleanly without traceback

### 7. Key Implementation Decisions

| Decision | Chosen Approach | Rationale |
|----------|-----------------|-----------|
| Data structure | `List[Task]` with `next_id` counter | Simple, ordered, matches spec requirements |
| ID generation | Sequential integer starting at 1 | Predictable, user-friendly |
| Task order | Creation order (oldest first) | Natural chronological display |
| Screen clearing | `os.system()` call | Cross-platform compatible |
| Input method | Standard `input()` | No external dependencies |
| Exception hierarchy | Custom exceptions inheriting from `Exception` | Clear error categories, testable |
| Type hints | Full type annotations | Python 3.11+ requirement |

---

## Complexity Tracking

*Not applicable. No Constitution Check violations require justification.*
