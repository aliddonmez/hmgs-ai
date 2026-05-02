import os
import sys
import csv
import re
import hashlib
from pathlib import Path
from typing import List

from dotenv import load_dotenv
import psycopg
from psycopg.types.json import Json
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
load_dotenv(dotenv_path=str(ROOT / ".env"))

from document_parser.pdf_loader import load_document_text
from document_parser.text_cleaner import clean_text
from document_parser.fallback_chunker import chunk_text
from document_parser.statute_parser import parse_statute_articles


# -------------------------------------------------
# Embedding model cache
# -------------------------------------------------

_MODEL = None


def get_model() -> SentenceTransformer:
    global _MODEL
    if _MODEL is None:
        model_name = os.getenv(
            "EMBED_MODEL",
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        )
        print(f"Loading embedding model: {model_name}")
        _MODEL = SentenceTransformer(model_name)
    return _MODEL


# -------------------------------------------------
# Postgres connection
# -------------------------------------------------


def pg_conn():
    return psycopg.connect(
        host=os.getenv("PG_HOST", "localhost"),
        port=int(os.getenv("PG_PORT", "5432")),
        dbname=os.getenv("PG_DB", "postgres"),
        user=os.getenv("PG_USER", "postgres"),
        password=os.getenv("PG_PASSWORD", ""),
    )


# -------------------------------------------------
# File hash
# -------------------------------------------------


def file_hash(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


# -------------------------------------------------
# Embedding
# -------------------------------------------------


def embed_texts(texts: List[str], batch_size: int = 64):
    if not texts:
        return []

    model = get_model()
    embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        emb = model.encode(batch, normalize_embeddings=True)
        embeddings.extend(emb)

    return [e.tolist() for e in embeddings]


# -------------------------------------------------
# Chunk metadata
# -------------------------------------------------


def build_chunk_meta(
    doc_id: str,
    chunk_index: int,
    content: str,
    article: dict | None = None,
) -> dict:
    meta = {
        "source": doc_id,
        "chunk_index": chunk_index,
        "kanun": "TCK",
        "madde_no": None,
        "title": None,
        "full_heading": None,
        "chunk_type": "article",
    }

    # Parser'dan article bilgisi geldiyse önce onu kullan
    if article:
        title = article.get("title")
        if title:
            meta["full_heading"] = title

            madde_match = re.search(r"Madde\s+(\d+)", title, re.IGNORECASE)
            if madde_match:
                meta["madde_no"] = madde_match.group(1)

            # Örnek:
            # "TCK Madde 141 - Hırsızlık" -> "Hırsızlık"
            parts = title.split(" - ")
            if len(parts) >= 2:
                meta["title"] = parts[1].strip()
            else:
                meta["title"] = title.strip()

        return meta

    # Fallback: content içinden çıkarmaya çalış
    match = re.search(r"(TCK\s+Madde\s+(\d+)\s*-\s*([^-\n]+))", content, re.IGNORECASE)
    if match:
        meta["full_heading"] = match.group(1).strip()
        meta["madde_no"] = match.group(2).strip()
        meta["title"] = match.group(3).strip()

    return meta


# -------------------------------------------------
# Ingest manifest
# -------------------------------------------------


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

        # Dosya oku + genel temizlik
        text = load_document_text(path)
        text = clean_text(text)

        h = file_hash(path)

        article_payloads = None

        # PDF için önce madde parser dene
        if ext == ".pdf":
            articles = parse_statute_articles(text)

            if len(articles) > 3:
                print(f"{doc_id}: statute parser used ({len(articles)} articles)")
                article_payloads = []
                chunks = []

                for a in articles:
                    chunk_content = f'{a["title"]} - {a["content"]}'
                    chunks.append(chunk_content)
                    article_payloads.append(a)
            else:
                print(f"{doc_id}: fallback chunking")
                chunks = chunk_text(text)
        else:
            chunks = chunk_text(text)

        docs.append((doc_id, ders, konu, title, path, mime, h, chunks, article_payloads))

    # -------------------------------------------------
    # Chunk listesi oluştur
    # -------------------------------------------------

    all_chunks = []
    chunk_map = []

    for doc_id, _, _, _, _, _, _, chunks, article_payloads in docs:
        for idx, ch in enumerate(chunks):
            all_chunks.append(ch)

            article = None
            if article_payloads and idx < len(article_payloads):
                article = article_payloads[idx]

            chunk_map.append((doc_id, idx, article))

    print("TOTAL CHUNKS:", len(all_chunks))

    embeddings = embed_texts(all_chunks) if all_chunks else []

    print("TOTAL EMBEDDINGS:", len(embeddings))

    # -------------------------------------------------
    # DB write
    # -------------------------------------------------

    with pg_conn() as conn:
        with conn.cursor() as cur:
            for doc_id, ders, konu, title, path, mime, h, _chunks, _article_payloads in docs:
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

                cur.execute(
                    "DELETE FROM document_chunks WHERE document_id = %s;",
                    (doc_id,),
                )

            for (doc_id, chunk_index, article), content, emb in zip(
                chunk_map, all_chunks, embeddings
            ):
                meta = build_chunk_meta(
                    doc_id=doc_id,
                    chunk_index=chunk_index,
                    content=content,
                    article=article,
                )

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


# -------------------------------------------------
# CLI
# -------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python scripts/ingest_documents.py data/imports/documents/manifest_vX.csv"
        )
        raise SystemExit(1)

    ingest_manifest(sys.argv[1])