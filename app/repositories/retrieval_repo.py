import os
from typing import List, Dict
from dotenv import load_dotenv
import psycopg

load_dotenv(dotenv_path=".env")

def pg_conn():
    return psycopg.connect(
        host=os.getenv("PG_HOST","localhost"),
        port=int(os.getenv("PG_PORT","5432")),
        dbname=os.getenv("PG_DB","postgres"),
        user=os.getenv("PG_USER","postgres"),
        password=os.getenv("PG_PASSWORD",""),
    )

def embed_query(text: str):
    from sentence_transformers import SentenceTransformer
    model_name = os.getenv("EMBED_MODEL","sentence-transformers/all-MiniLM-L6-v2")
    model = SentenceTransformer(model_name)
    return model.encode([text], normalize_embeddings=True).tolist()[0]

def search_chunks(query: str, top_k: int = 5, ders: str | None = None, konu: str | None = None) -> List[Dict]:
    q_emb = embed_query(query)

    where = []
    params = []

    # optional filters
    if ders:
        where.append("d.ders = %s")
        params.append(ders)
    if konu:
        where.append("d.konu = %s")
        params.append(konu)

    # keyword hint (çok yardımcı)
    # query'den 1-2 ana kelime çekelim (basit)
    kw = None
    qlow = query.lower()
    if "hırsız" in qlow or "hirsiz" in qlow:
        kw = "hırsız"
    elif "tck" in qlow:
        kw = "tck"

    if kw:
        where.append("dc.content ILIKE %s")
        params.append(f"%{kw}%")

    where_sql = ("WHERE " + " AND ".join(where)) if where else ""

    sql = f"""
    SELECT
        dc.document_id,
        d.title,
        d.ders,
        d.konu,
        dc.chunk_index,
        dc.content,
        (1 - (dc.embedding <=> %s::vector)) AS score
    FROM document_chunks dc
    JOIN documents d ON d.id = dc.document_id
    {where_sql}
    ORDER BY dc.embedding <=> %s::vector
    LIMIT %s;
    """

    # embedding paramları başta ve sonda
    final_params = [q_emb] + params + [q_emb, top_k]

    with pg_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, final_params)
            rows = cur.fetchall()

    results = []
    for r in rows:
        results.append({
            "document_id": r[0],
            "title": r[1],
            "ders": r[2],
            "konu": r[3],
            "chunk_index": r[4],
            "content": r[5],
            "score": float(r[6]),
        })
    return results
