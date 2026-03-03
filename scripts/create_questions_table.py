import os
from dotenv import load_dotenv
import psycopg

load_dotenv(dotenv_path=".env")

conn = psycopg.connect(
    host=os.getenv("PG_HOST","localhost"),
    port=int(os.getenv("PG_PORT","5432")),
    dbname=os.getenv("PG_DB","postgres"),
    user=os.getenv("PG_USER","postgres"),
    password=os.getenv("PG_PASSWORD",""),
)

with conn.cursor() as cur:
    cur.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id TEXT PRIMARY KEY,
        ders TEXT,
        konu TEXT,
        difficulty INTEGER,
        question_text TEXT NOT NULL,
        options JSONB NOT NULL,
        correct_index INTEGER NOT NULL,
        explanation TEXT,
        tags JSONB,
        source TEXT,
        version INTEGER DEFAULT 1,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """)

conn.commit()
conn.close()
print("QUESTIONS TABLE OK")
