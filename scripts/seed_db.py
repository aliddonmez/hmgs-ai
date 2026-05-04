# scripts/seed_db.py

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from sentence_transformers import SentenceTransformer
from psycopg.types.json import Json

from analysis.db import get_conn
from data.day2_texts import TEXTS as DAY2_TEXTS

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def vector_to_pgvector(values):
    """
    Python list[float] değerini pgvector formatına çevirir.
    Örnek: [0.1, 0.2, 0.3] -> "[0.1,0.2,0.3]"
    """
    return "[" + ",".join(str(float(v)) for v in values) + "]"


def main():
    conn = get_conn()
    cur = conn.cursor()

    # Geliştirme aşamasında eski kaynakları temizle.
    # documents tablosuna bağlı document_chunks kayıtları da CASCADE ile temizlenir.
    cur.execute("TRUNCATE TABLE documents RESTART IDENTITY CASCADE;")

    for i, item in enumerate(DAY2_TEXTS):
        doc_id = item.get("id", f"doc_{i + 1}")
        title = item.get("title", f"Belge {i + 1}")
        text = item.get("text", "")

        ders = item.get("ders")
        konu = item.get("konu")
        source = item.get("source", "seed_db")

        if not text or not text.strip():
            continue

        emb = model.encode(text).tolist()
        emb_vector = vector_to_pgvector(emb)

        # 1) documents tablosuna belge kaydı ekle
        cur.execute(
            """
            INSERT INTO documents (
                id,
                ders,
                konu,
                title,
                file_path,
                mime_type,
                file_hash
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                doc_id,
                ders,
                konu,
                title,
                source,
                "text/plain",
                None,
            ),
        )

        # 2) document_chunks tablosuna içerik + embedding ekle
        cur.execute(
            """
            INSERT INTO document_chunks (
                document_id,
                chunk_index,
                content,
                embedding,
                meta
            )
            VALUES (%s, %s, %s, %s::vector, %s)
            """,
            (
                doc_id,
                0,
                text,
                emb_vector,
                Json(
                    {
                        "source": source,
                        "title": title,
                        "ders": ders,
                        "konu": konu,
                    }
                ),
            ),
        )

    conn.commit()
    cur.close()
    conn.close()

    print("✅ DB hazır (documents + document_chunks + embedding tamamlandı)")


if __name__ == "__main__":
    main()
