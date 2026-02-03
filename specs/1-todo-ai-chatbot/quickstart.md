# Quickstart Guide: Todo AI Chatbot

## Prerequisites

- Python 3.11+
- Node.js 18+
- Neon Serverless PostgreSQL account
- OpenAI API key
- MCP SDK compatible environment

## Setup

### Backend Setup

1. Install Python dependencies:
```bash
pip install fastapi uvicorn sqlmodel openai python-multipart
```

2. Set environment variables:
```bash
export DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname"
export OPENAI_API_KEY="sk-..."
export MCP_SERVER_URL="http://localhost:8000/mcp"
```

3. Initialize the database:
```bash
python -c "from src.database import create_db_and_tables; create_db_and_tables()"
```

4. Start the backend server:
```bash
uvicorn src.main:app --reload
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
npm install @openai/chatkit
```

2. Configure ChatKit:
```typescript
// Set environment variables in .env
VITE_CHATKIT_API_URL=http://localhost:8000/api
```

3. Start the frontend:
```bash
npm run dev
```

## Usage

1. Navigate to the frontend URL (typically http://localhost:5173)
2. Enter your user ID (for demo purposes, you can use any UUID)
3. Start chatting with the AI bot using natural language:
   - "Add a task to buy groceries"
   - "Show me my tasks"
   - "Complete the meeting task"
   - "Delete my old task"

## API Endpoints

- `POST /api/{user_id}/chat` - Main chat endpoint
- `GET /health` - Health check endpoint

## MCP Server

The MCP server runs separately and exposes the following tools:
- `add_task` - Create new tasks
- `list_tasks` - Retrieve user tasks
- `update_task` - Modify existing tasks
- `complete_task` - Mark tasks as completed
- `delete_task` - Remove tasks

## Development

To run tests:
```bash
# Backend tests
pytest tests/

# Frontend tests
npm run test
```