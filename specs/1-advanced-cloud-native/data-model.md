# Data Model: Advanced Cloud-Native Todo AI Platform

**Feature**: Advanced Cloud-Native Todo AI Platform
**Date**: 2026-02-04
**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

## Entity Models

### Task (Extended from Phase III)
**Description**: Represents a user's task with advanced features
**Fields**:
- `id`: UUID (primary key)
- `user_id`: UUID (foreign key to user)
- `title`: String (255 chars max)
- `description`: Text (optional)
- `status`: Enum ['pending', 'in-progress', 'completed'] (default: 'pending')
- `priority`: Enum ['low', 'medium', 'high', 'urgent'] (default: 'medium')
- `due_date`: DateTime (nullable, timezone-aware)
- `created_at`: DateTime (auto-generated)
- `updated_at`: DateTime (auto-generated)
- `completed_at`: DateTime (nullable)
- `tags`: JSON array of strings (max 10 tags, 50 chars each)
- `recurrence_rule`: String (nullable, RFC 5545 format)
- `parent_task_id`: UUID (nullable, foreign key to self for recurring instances)

**Validation Rules**:
- Title is required and non-empty
- Priority must be one of the defined enum values
- Due date cannot be in the past when setting
- Tags array cannot exceed 10 items
- Each tag cannot exceed 50 characters
- Recurrence rule must follow RFC 5545 format when present

**State Transitions**:
- `pending` → `in-progress` (when started)
- `in-progress` → `pending` (when paused)
- `in-progress` → `completed` (when finished)
- `completed` → `pending` (when reopened)

### TaskTemplate (New for Phase V)
**Description**: Defines recurrence patterns for generating recurring task instances
**Fields**:
- `id`: UUID (primary key)
- `user_id`: UUID (foreign key to user)
- `base_task_id`: UUID (foreign key to Task - the template basis)
- `recurrence_rule`: String (RFC 5545 format, required)
- `ends_on`: DateTime (nullable, when recurrence should stop)
- `occurrence_count`: Integer (nullable, max number of occurrences)
- `created_at`: DateTime (auto-generated)
- `updated_at`: DateTime (auto-generated)
- `is_active`: Boolean (default: true)

**Validation Rules**:
- Base task must exist and be valid
- Recurrence rule must follow RFC 5545 format
- Ends_on and occurrence_count cannot both be null (infinite recurrences not allowed)
- Is_active can only be set to false, not reactivated

### ScheduledReminder (New for Phase V)
**Description**: Represents a scheduled notification for upcoming due dates
**Fields**:
- `id`: UUID (primary key)
- `task_id`: UUID (foreign key to Task)
- `user_id`: UUID (foreign key to user)
- `scheduled_time`: DateTime (when notification should be sent)
- `notification_method`: Enum ['email', 'push', 'sms'] (default: 'push')
- `is_sent`: Boolean (default: false)
- `sent_at`: DateTime (nullable, when sent)
- `created_at`: DateTime (auto-generated)

**Validation Rules**:
- Task must exist and have a due_date
- Scheduled_time must be before the task's due_date
- Notification_method must be one of the defined enum values
- Cannot create reminder for completed tasks

### TaskEvent (New for Phase V)
**Description**: Immutable record of task lifecycle events for event sourcing
**Fields**:
- `id`: UUID (primary key)
- `task_id`: UUID (foreign key to Task)
- `event_type`: Enum ['created', 'updated', 'status_changed', 'deleted', 'completed', 'reopened']
- `payload`: JSON (event-specific data)
- `timestamp`: DateTime (auto-generated, timezone-aware)
- `correlation_id`: UUID (for tracking related events)
- `causation_id`: UUID (nullable, for tracking causality)

**Validation Rules**:
- Event type must be one of the defined enum values
- Payload must be valid JSON
- Timestamp is auto-generated and cannot be modified
- Correlation_id is required for all events

### AuditLog (New for Phase V)
**Description**: Persistent log of all system events for compliance and debugging
**Fields**:
- `id`: UUID (primary key)
- `event_type`: String (type of event)
- `entity_id`: UUID (nullable, ID of affected entity)
- `entity_type`: String (type of entity affected)
- `user_id`: UUID (nullable, user who triggered event)
- `action`: String (what happened)
- `old_values`: JSON (nullable, previous state)
- `new_values`: JSON (nullable, new state)
- `timestamp`: DateTime (auto-generated, timezone-aware)
- `metadata`: JSON (nullable, additional context)

**Validation Rules**:
- Event type and action must be non-empty
- Timestamp is auto-generated and cannot be modified
- Metadata must be valid JSON when present

## Relationships

```
User --(1:N)-- Task
User --(1:N)-- TaskTemplate
User --(1:N)-- ScheduledReminder

Task --(1:N)-- TaskEvent (via task_id)
Task --(1:1)-- ScheduledReminder (via task_id, optional)

Task --(1:1)-- TaskTemplate (via parent_task_id, for recurring instances)
TaskTemplate --(1:N)-- Task (via base_task_id, for templates)

AuditLog --(N:1)-- User (via user_id, nullable)
AuditLog --(N:1)-- Task (via entity_id when entity_type='Task', nullable)
```

## Indexes

**Task Table**:
- Primary: `id`
- Composite: `(user_id, status, created_at)` for user task queries
- Composite: `(user_id, due_date)` for due date queries
- Individual: `due_date` for scheduling queries
- Individual: `recurrence_rule` for recurrence queries
- Individual: `parent_task_id` for recurring task queries

**TaskTemplate Table**:
- Primary: `id`
- Individual: `base_task_id` for template lookup
- Individual: `user_id` for user queries
- Individual: `is_active` for active templates

**ScheduledReminder Table**:
- Primary: `id`
- Individual: `scheduled_time` for scheduling queries
- Individual: `is_sent` for unsent reminders
- Individual: `task_id` for task-related queries

**TaskEvent Table**:
- Primary: `id`
- Individual: `task_id` for task events
- Individual: `timestamp` for chronological queries
- Individual: `event_type` for filtering events

**AuditLog Table**:
- Primary: `id`
- Individual: `timestamp` for chronological queries
- Individual: `entity_type` for filtering by entity
- Individual: `user_id` for user activity
- Individual: `event_type` for filtering by event type

## Constraints

- **Task**: Prevent setting due_date in the past
- **TaskTemplate**: Prevent infinite recurrence (require either ends_on or occurrence_count)
- **ScheduledReminder**: Prevent creating reminders for completed tasks
- **TaskEvent**: Immutable records (no updates allowed)
- **Referential Integrity**: Foreign key constraints enforce relationships
- **Data Consistency**: JSON fields validated for proper format