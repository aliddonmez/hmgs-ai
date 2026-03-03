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
    CREATE TABLE IF NOT EXISTS documents (
        id TEXT PRIMARY KEY,
        ders TEXT,
        konu TEXT,
        title TEXT,
        file_path TEXT NOT NULL,
        mime_type TEXT,
        file_hash TEXT,
        version INTEGER DEFAULT 1,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """)

    # embedding column: vector(384) MiniLM-L6-v2 için tipik boyut 384
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS document_chunks (
        id BIGSERIAL PRIMARY KEY,
        document_id TEXT REFERENCES documents(id) ON DELETE CASCADE,
        chunk_index INTEGER NOT NULL,
        content TEXT NOT NULL,
        embedding vector(384),
        meta JSONB,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_doc_chunks_doc ON document_chunks(document_id);")
    # Vector index (ivfflat) — daha sonra veri büyüyünce hız için
    # cur.execute("CREATE INDEX IF NOT EXISTS idx_doc_chunks_vec ON document_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);")

conn.commit()
conn.close()
print("DOCUMENT TABLES OK")
