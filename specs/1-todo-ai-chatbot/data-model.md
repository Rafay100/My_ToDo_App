# Data Model: Todo AI Chatbot

## Entities

### User
- **Description**: Represents a registered user of the system
- **Fields**:
  - id: UUID (primary key)
  - email: String (unique, indexed)
  - created_at: DateTime (indexed)
  - updated_at: DateTime
- **Relationships**:
  - Has many: tasks, conversations
- **Validation**:
  - Email must be valid format
  - Email must be unique

### Task
- **Description**: Represents a todo item managed by the user
- **Fields**:
  - id: UUID (primary key)
  - user_id: UUID (foreign key to User, indexed)
  - title: String (max 255 chars)
  - description: Text (optional)
  - status: Enum ('active', 'completed') (indexed)
  - created_at: DateTime (indexed)
  - updated_at: DateTime
  - completed_at: DateTime (nullable)
- **Relationships**:
  - Belongs to: user
- **Validation**:
  - Title is required
  - Status must be one of allowed values
  - Completed_at must be null if status is not 'completed'

### Conversation
- **Description**: Represents a collection of messages between a user and the AI agent
- **Fields**:
  - id: UUID (primary key)
  - user_id: UUID (foreign key to User, indexed)
  - title: String (auto-generated from first message or user-specified)
  - created_at: DateTime (indexed)
  - updated_at: DateTime
- **Relationships**:
  - Belongs to: user
  - Has many: messages
- **Validation**:
  - User_id is required

### Message
- **Description**: Represents an individual message in a conversation
- **Fields**:
  - id: UUID (primary key)
  - conversation_id: UUID (foreign key to Conversation, indexed)
  - role: Enum ('user', 'assistant', 'system')
  - content: Text
  - created_at: DateTime (indexed)
  - metadata: JSON (optional, for storing AI-related data)
- **Relationships**:
  - Belongs to: conversation
- **Validation**:
  - Conversation_id is required
  - Role must be one of allowed values
  - Content is required

## Indexes
- User.email (unique)
- User.created_at
- Task.user_id
- Task.status
- Task.created_at
- Conversation.user_id
- Conversation.created_at
- Message.conversation_id
- Message.role
- Message.created_at

## Relationships
- User 1---* Task (one-to-many)
- User 1---* Conversation (one-to-many)
- Conversation 1---* Message (one-to-many)