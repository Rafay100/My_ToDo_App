# Evolution of Todo - Phase III (AI-Powered Chatbot)

A stateless AI-powered todo chatbot that allows users to manage their tasks through natural language using OpenAI Agents SDK and MCP tools.

## Tech Stack

- **Backend**: Python (FastAPI), SQLModel (ORM), OpenAI SDK
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK
- **Database**: Neon Serverless PostgreSQL
- **Frontend**: Next.js 14+, OpenAI ChatKit
- **Infrastructure**: Alembic (Migrations)

## Features

- Natural language processing for todo management
- Conversational UI using OpenAI ChatKit
- Stateless architecture with no in-memory session state
- MCP tools for task operations (add, list, update, complete, delete)
- Database persistence for conversations and tasks

## Quickstart

### 1. Database Setup
- Create a project on [Neon.tech](https://neon.tech)
- Copy the connection string (with pooled connection enabled)

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
# Export DATABASE_URL and OPENAI_API_KEY
uvicorn src.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
# Set NEXT_PUBLIC_API_URL in .env.local
npm run dev
```

## API Endpoints

- `POST /api/{user_id}/chat` - Main chat endpoint for AI interactions
- `GET /health` - Health check endpoint
- `GET /api/{user_id}/conversations/{conversation_id}` - Get conversation history

## Phase Isolation

This project follows strictly isolated phases. Phase III introduces AI and agents as specified in the constitution.

## Architecture

The system follows a stateless architecture where:
- All AI state is persisted in the database
- No server-side session memory is used
- All conversations and messages are stored in the database
- The AI agent operates per request without maintaining state between requests

## MCP Tools

The system exposes the following MCP tools:
- `add_task` - Create new tasks
- `list_tasks` - Retrieve user tasks
- `update_task` - Modify existing tasks
- `complete_task` - Mark tasks as completed
- `delete_task` - Remove tasks

## Development

To run tests:
```bash
# Backend tests
cd backend
pytest tests/
```

## Contributing

This project follows the Spec-Driven Development methodology. All changes must originate from an approved specification.

## License

MIT