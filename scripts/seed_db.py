# scripts/seed_db.py

import os
import sys

# ✅ Proje root'unu Python path'ine ekle (analysis/ paketini bulsun)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from sentence_transformers import SentenceTransformer
from analysis.db import get_conn
from data.day2_texts import TEXTS as DAY2_TEXTS

# 🔹 Embedding modeli
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def main():
    conn = get_conn()
    cur = conn.cursor()

    # ⚠️ GELİŞTİRME AŞAMASINDA:
    cur.execute("DELETE FROM hukuki_kaynaklar;")

    for item in TEXTS:
        emb = model.encode(item["text"]).tolist()
        cur.execute(
            """
            INSERT INTO hukuki_kaynaklar (title, content, embedding)
            VALUES (%s, %s, %s)
            """,
            (item["title"], item["text"], emb),
        )

    conn.commit()
    cur.close()
    conn.close()

    print("✅ DB hazır (embedding + indexing tamamlandı)")


if __name__ == "__main__":
    main()
