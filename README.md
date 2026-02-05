# TaskFlow AI - Spec-Driven Todo Application

## Project Structure

This project follows the Spec-Kit methodology for spec-driven development:

```
├── specs/                 # Feature specifications
│   └── todo-app/         # Todo application feature
│       ├── spec.md       # Feature requirements
│       ├── plan.md       # Architecture & implementation plan
│       ├── tasks.md      # Implementation tasks
│       └── intelligence/ # Requirements & research
├── history/              # Development artifacts
│   ├── specs/           # Historical specs
│   ├── plans/           # Historical plans
│   ├── tasks/           # Historical tasks
│   ├── adrs/            # Architectural decision records
│   └── prompts/         # AI interaction history
├── frontend/            # Frontend application
└── backend/             # Backend API
```

## Development Phases

1. **Specification Phase**: Define requirements in `specs/todo-app/spec.md`
2. **Planning Phase**: Design architecture in `specs/todo-app/plan.md`
3. **Implementation Phase**: Execute tasks in `specs/todo-app/tasks.md`

## Quick Start

### Backend (API Server)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
# Set DATABASE_URL and OPENAI_API_KEY environment variables
uvicorn src.main:app --reload --port 8000
```

### Frontend (Web Application)
```bash
cd frontend
npm install
# Set NEXT_PUBLIC_API_URL in .env.local
npm run dev
```

Both servers must run simultaneously for full functionality.

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

## Contributing

This project follows the Spec-Driven Development methodology. All changes must originate from an approved specification.

## License

MIT