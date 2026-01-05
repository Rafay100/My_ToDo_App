import sys
from pathlib import Path

# Add backend src to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir / "src"))

from dotenv import load_dotenv
load_dotenv(backend_dir / ".env")

from sqlalchemy import text
from src.db import engine

if __name__ == "__main__":
    # Drop tables
    print("Dropping tables...")
    with engine.connect() as conn:
        conn.execute(text('DROP TABLE IF EXISTS "todo" CASCADE'))
        conn.execute(text('DROP TABLE IF EXISTS "user" CASCADE'))
        conn.commit()

    # Create tables with explicit types
    print("Creating tables...")
    with engine.connect() as conn:
        # Create user table with explicit VARCHAR(255) for password
        conn.execute(text('''
            CREATE TABLE "user" (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                email VARCHAR(255) UNIQUE NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        '''))

        # Create todo table
        conn.execute(text('''
            CREATE TABLE "todo" (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID NOT NULL REFERENCES "user"(id),
                title VARCHAR(255) NOT NULL,
                is_completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            )
        '''))

        conn.commit()

    print("Tables created successfully!")
