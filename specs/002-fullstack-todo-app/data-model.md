# Data Model: Phase II Full-Stack Todo App

**Feature**: 002-fullstack-todo-app
**Database**: Neon Serverless PostgreSQL

## Entities

### 1. User
Represents an authenticated individual.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key | Unique identifier |
| email | String | Unique, Not Null | Authentication identifier |
| hashed_password | String | Not Null | Securely stored password |
| created_at | DateTime | Not Null | Registration timestamp |

### 2. Todo
Represents a single task associated with a user.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key | Unique identifier |
| user_id | UUID | Foreign Key (User) | Owner of the todo |
| title | String | Not Null | Task description |
| is_completed | Boolean | Default: False | Completion status |
| created_at | DateTime | Not Null | Creation timestamp |
| updated_at | DateTime | Not Null | Last modification timestamp |

## Relationships
- **User (1) <---> Todo (*)**: One user can have many todos. Todos belong to exactly one user.

## Validation Rules
- **Todo Title**: Must be between 1 and 255 characters. Cannot be empty or whitespace only.
- **User Email**: Must be a valid email format.
- **User Password**: Must be at least 8 characters long.
