import os
import sys
import csv
import hashlib
from pathlib import Path
from typing import List
from dotenv import load_dotenv
import psycopg
from psycopg.types.json import Json

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
load_dotenv(dotenv_path=str(ROOT / ".env"))

def pg_conn():
    return psycopg.connect(
        host=os.getenv("PG_HOST","localhost"),
        port=int(os.getenv("PG_PORT","5432")),
        dbname=os.getenv("PG_DB","postgres"),
        user=os.getenv("PG_USER","postgres"),
        password=os.getenv("PG_PASSWORD",""),
    )

def file_hash(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_text_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()

    if ext == ".txt":
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    if ext == ".pdf":
        import fitz  # pymupdf
        doc = fitz.open(path)
        parts = []
        for page in doc:
            parts.append(page.get_text("text"))
        return "\n".join(parts)

    if ext == ".docx":
        import docx
        d = docx.Document(path)
        return "\n".join(p.text for p in d.paragraphs)

    raise ValueError(f"Unsupported file type: {ext}")

def chunk_text(text: str, max_chars: int = 900, overlap: int = 150) -> List[str]:
    text = text.strip()
    if not text:
        return []
    chunks = []
    i = 0
    while i < len(text):
        end = min(len(text), i + max_chars)
        chunks.append(text[i:end])
        i = end - overlap
        if i < 0:
            i = 0
        if end == len(text):
            break
    return chunks

def embed_texts(texts: List[str]):
    from sentence_transformers import SentenceTransformer
    model_name = os.getenv("EMBED_MODEL","sentence-transformers/all-MiniLM-L6-v2")
    model = SentenceTransformer(model_name)
    return model.encode(texts, normalize_embeddings=True).tolist()

def ingest_manifest(manifest_csv: str):
    with open(manifest_csv, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    docs = []
    for r in rows:
        doc_id = r["doc_id"]
        ders = r.get("ders")
        konu = r.get("konu")
        title = r.get("title")
        path = r["file_path"]

        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing file: {path}")

        ext = os.path.splitext(path)[1].lower()
        mime = {
            ".txt": "text/plain",
            ".pdf": "application/pdf",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }.get(ext, "application/octet-stream")

        text = read_text_file(path)
        h = file_hash(path)
        chunks = chunk_text(text)
        docs.append((doc_id, ders, konu, title, path, mime, h, chunks))

    all_chunks = []
    chunk_map = []
    for doc_id, _, _, _, _, _, _, chunks in docs:
        for idx, ch in enumerate(chunks):
            all_chunks.append(ch)
            chunk_map.append((doc_id, idx))

    embeddings = embed_texts(all_chunks) if all_chunks else []

    with pg_conn() as conn:
        with conn.cursor() as cur:
            for doc_id, ders, konu, title, path, mime, h, _chunks in docs:
                cur.execute(
                    """
                    INSERT INTO documents
                    (id, ders, konu, title, file_path, mime_type, file_hash, version)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,1)
                    ON CONFLICT (id) DO UPDATE SET
                        ders=EXCLUDED.ders,
                        konu=EXCLUDED.konu,
                        title=EXCLUDED.title,
                        file_path=EXCLUDED.file_path,
                        mime_type=EXCLUDED.mime_type,
                        file_hash=EXCLUDED.file_hash;
                    """,
                    (doc_id, ders, konu, title, path, mime, h),
                )
                cur.execute("DELETE FROM document_chunks WHERE document_id = %s;", (doc_id,))

            for i, ((doc_id, chunk_index), content) in enumerate(zip(chunk_map, all_chunks)):
                emb = embeddings[i]
                meta = {"chunk_index": chunk_index}
                cur.execute(
                    """
                    INSERT INTO document_chunks
                    (document_id, chunk_index, content, embedding, meta)
                    VALUES (%s,%s,%s,%s,%s);
                    """,
                    (doc_id, chunk_index, content, emb, Json(meta)),
                )

        conn.commit()

    print(f"Ingested {len(docs)} documents, {len(all_chunks)} chunks.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/ingest_documents.py data/imports/documents/manifest_vX.csv")
        raise SystemExit(1)
    ingest_manifest(sys.argv[1])
