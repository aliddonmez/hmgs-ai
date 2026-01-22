import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from data.day2_texts import TEXTS
from sentence_transformers import SentenceTransformer
import psycopg


def main():
    # Embedding modeli
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    # PostgreSQL bağlantısı
    conn = psycopg.connect(
        host="localhost",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="1234"
    )

    cur = conn.cursor()

    # Tabloyu temizle
    cur.execute("DELETE FROM public.hukuki_kaynaklar;")


    # Metinleri DB'ye yaz
    for item in TEXTS:
        emb = model.encode(item["text"]).tolist()
        cur.execute(
            """
            INSERT INTO hukuki_kaynaklar (title, content, embedding)
            VALUES (%s, %s, %s)
            """,
            (item["title"], item["text"], emb)
        )

    conn.commit()
    print("📥 Metinler DB'ye kaydedildi")

    # Soru
    question = "Hırsızlık suçu nedir?"
    q_emb = model.encode(question).tolist()

    # Vector search
    cur.execute(
        """
        SELECT
            title,
            1 - (embedding <=> %s::vector) AS similarity
        FROM hukuki_kaynaklar
        ORDER BY embedding <=> %s::vector
        LIMIT 10
        """,
        (q_emb, q_emb)
    )

    print("\nQUESTION:", question)
    print("-" * 70)
    for title, score in cur.fetchall():
        print(f"{score:.4f} | {title}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
