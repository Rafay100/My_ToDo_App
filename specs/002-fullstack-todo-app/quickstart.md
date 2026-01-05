# Quickstart: Phase II Full-Stack Todo App

## Prerequisites
- Python 3.11+
- Node.js 18+
- Neon DB Account and Database URL

## Local Setup

### 1. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install fastapi sqlmodel uvicorn alembic psycopg2-binary
cp .env.example .env  # Configure DATABASE_URL
alembic upgrade head
uvicorn src.main:app --reload
```

### 2. Frontend
```bash
cd frontend
npm install
cp .env.example .env.local  # Configure NEXT_PUBLIC_API_URL
npm run dev
```

## URLs
- **API Docs**: http://localhost:8000/docs
- **Web App**: http://localhost:3000
