import os
from pathlib import Path
from dotenv import load_dotenv
from sqlmodel import create_engine, Session

# Load .env from backend directory
backend_dir = Path(__file__).parent.parent
load_dotenv(backend_dir / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

# Check for Neon DB specific requirements (require sslmode=require)
if DATABASE_URL and "sslmode=" not in DATABASE_URL and "postgresql" in DATABASE_URL:
    if "?" in DATABASE_URL:
        DATABASE_URL += "&sslmode=require"
    else:
        DATABASE_URL += "?sslmode=require"

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session
