from sqlmodel import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv('DATABASE_URL'))

with engine.connect() as conn:
    # Add the name column to the user table
    conn.execute(text("ALTER TABLE \"user\" ADD COLUMN IF NOT EXISTS name VARCHAR"))
    conn.commit()
    print("Added 'name' column to 'user' table")

    # Verify the change
    result = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'user' ORDER BY ordinal_position"))
    print("\nUpdated 'user' table columns:")
    for row in result:
        print(f"  {row[0]}: {row[1]}")
