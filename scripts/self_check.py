import os
import sys
from dotenv import load_dotenv

print("=== HMGS SELF CHECK START ===\n")

# 1️⃣ ENV + PG bağlantı testi
print("1) Postgres bağlantı testi...")
try:
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
        cur.execute("SELECT 1;")
        print("   ✔ PG bağlantı OK")
    conn.close()
except Exception as e:
    print("   ❌ PG bağlantı FAIL:", e)
    sys.exit(1)

# 2️⃣ Tablolar ve sayım testi
print("\n2) Veri tabloları testi...")
tables = ["questions","cases","documents","document_chunks"]
try:
    conn = psycopg.connect(
        host=os.getenv("PG_HOST","localhost"),
        port=int(os.getenv("PG_PORT","5432")),
        dbname=os.getenv("PG_DB","postgres"),
        user=os.getenv("PG_USER","postgres"),
        password=os.getenv("PG_PASSWORD",""),
    )
    with conn.cursor() as cur:
        for t in tables:
            cur.execute(f"SELECT COUNT(*) FROM {t};")
            cnt = cur.fetchone()[0]
            print(f"   ✔ {t}: {cnt}")
    conn.close()
except Exception as e:
    print("   ❌ Tablo testi FAIL:", e)
    sys.exit(1)

# 3️⃣ Repo testi
print("\n3) Repository testi...")
try:
    sys.path.append(".")
    from app.repositories.questions_repo import get_questions
    from app.repositories.cases_repo import get_cases
    from app.repositories.retrieval_repo import search_chunks

    qs = get_questions()
    cs = get_cases()
    hits = search_chunks("Hırsızlık suçu hangi maddede düzenlenmiştir?", top_k=1)

    print(f"   ✔ questions_repo: {len(qs)} kayıt")
    print(f"   ✔ cases_repo: {len(cs)} kayıt")
    print(f"   ✔ retrieval top: {hits[0]['document_id'] if hits else 'EMPTY'}")

except Exception as e:
    print("   ❌ Repo testi FAIL:", e)
    sys.exit(1)

print("\n=== ✅ SELF CHECK PASSED ===")
