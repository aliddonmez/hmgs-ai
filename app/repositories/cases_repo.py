import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

def _pg_conn():
    import psycopg
    return psycopg.connect(
        host=os.getenv("PG_HOST","localhost"),
        port=int(os.getenv("PG_PORT","5432")),
        dbname=os.getenv("PG_DB","postgres"),
        user=os.getenv("PG_USER","postgres"),
        password=os.getenv("PG_PASSWORD",""),
    )

def get_cases() -> List[Dict]:
    try:
        with _pg_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT to_regclass('public.cases');")
                (reg,) = cur.fetchone()
                if not reg:
                    return []

                cur.execute("SELECT COUNT(*) FROM cases;")
                (cnt,) = cur.fetchone()
                if not cnt or cnt <= 0:
                    return []

                cur.execute("""
                    SELECT id, ders, konu, title, case_text, tags, source
                    FROM cases
                    ORDER BY id;
                """)
                rows = cur.fetchall()

                return [
                    {
                        "case_id": r[0],
                        "ders": r[1],
                        "konu": r[2],
                        "title": r[3],
                        "case_text": r[4],
                        "tags": r[5],
                        "source": r[6],
                    }
                    for r in rows
                ]
    except Exception as e:
        print(f"[cases_repo] DB read failed. Error: {e}")
        return []
