##seed_db.py
import sys
import os

# Proje root'unu Python path'ine ekle
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sentence_transformers import SentenceTransformer
import psycopg
from data.day2_texts import TEXTS


# 🔹 Embedding modeli
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# 🔹 PostgreSQL bağlantısı
conn = psycopg.connect(
    host="localhost",
    port=5433,
    dbname="postgres",
    user="postgres",
    password="1234"
)

cur = conn.cursor()


# ⚠️ GELİŞTİRME AŞAMASINDA:
# tabloyu temizle (prod'da ASLA böyle yapma)
cur.execute("DELETE FROM hukuki_kaynaklar;")


# 🔹 Metinleri embedding + insert
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

cur.close()
conn.close()

print("✅ DB hazır (embedding + indexing tamamlandı)")
