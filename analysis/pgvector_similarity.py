##pgvector_similarity
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from data.day2_texts import TEXTS
from sentence_transformers import SentenceTransformer
import psycopg

# 🔹 Global embedding modeli
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# 🔹 RAG'de kullanılacak TEK fonksiyon
def retrieve(question, top_k=5):
    conn = psycopg.connect(
        host="localhost",
        port=5433,
        dbname="postgres",
        user="postgres",
        password="1234"
    )
    cur = conn.cursor()

    q_emb = model.encode(question).tolist()

    cur.execute(
        """
        SELECT
            title,
            content,
            1 - (embedding <=> %s::vector) AS similarity
        FROM hukuki_kaynaklar
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        """,
        (q_emb, q_emb, top_k)
    )

    results = cur.fetchall()

    cur.close()
    conn.close()

    return results


# ======================================================
# 🧪 AŞAĞISI SADECE TEST / SEED AMAÇLIDIR (PASİF)
# ======================================================

"""
def main():
    conn = psycopg.connect(
        host="localhost",
        port=5433,
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
            '''
            INSERT INTO hukuki_kaynaklar (title, content, embedding)
            VALUES (%s, %s, %s)
            ''',
            (item["title"], item["text"], emb)
        )

    conn.commit()
    print("📥 Metinler DB'ye kaydedildi")

    # Test sorusu
    question = "Hırsızlık suçu nedir?"
    q_emb = model.encode(question).tolist()

    cur.execute(
        '''
        SELECT
            title,
            1 - (embedding <=> %s::vector) AS similarity
        FROM hukuki_kaynaklar
        ORDER BY embedding <=> %s::vector
        LIMIT 10
        ''',
        (q_emb, q_emb)
    )

    print("\\nQUESTION:", question)
    print("-" * 70)
    for title, score in cur.fetchall():
        print(f"{score:.4f} | {title}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
"""
