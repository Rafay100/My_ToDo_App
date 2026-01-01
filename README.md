# Evolution of Todo - Phase II (Full-Stack)

A full-stack web application for task management.

## Tech Stack
- **Backend**: Python (FastAPI), SQLModel (ORM)
- **Database**: Neon Serverless PostgreSQL
- **Frontend**: Next.js 14+ (TypeScript), Better Auth
- **Infrastructure**: Alembic (Migrations)

## Quickstart

### 1. Database Setup
- Create a project on [Neon.tech](https://neon.tech)
- Copy the connection string (with pooled connection enabled)

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venvScriptsactivate
pip install -r requirements.txt
# Export DATABASE_URL and SECRET_KEY
uvicorn src.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
# Set NEXT_PUBLIC_API_URL and DATABASE_URL in .env.local
npm run dev
```

## Phase Isolation
This project follows strictly isolated phases. Phase III will introduce AI and agents.
🤖 Generated with [Claude Code](https://claude.com)
