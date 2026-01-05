from sqlmodel import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv('DATABASE_URL'))

with engine.connect() as conn:
    result = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'user' ORDER BY ordinal_position"))
    print("\nCurrent 'user' table columns:")
    for row in result:
        print(f"  {row[0]}: {row[1]}")
