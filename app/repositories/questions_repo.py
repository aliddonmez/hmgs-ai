import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


def _pg_conn():
    import psycopg

    return psycopg.connect(
        host=os.getenv("PG_HOST", "localhost"),
        port=int(os.getenv("PG_PORT", "5432")),
        dbname=os.getenv("PG_DB", "postgres"),
        user=os.getenv("PG_USER", "postgres"),
        password=os.getenv("PG_PASSWORD", ""),
    )


def get_questions() -> List[Dict]:
    try:
        with _pg_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT to_regclass('public.questions');")
                (reg,) = cur.fetchone()

                if reg:
                    cur.execute("SELECT COUNT(*) FROM questions;")
                    (cnt,) = cur.fetchone()

                    if cnt and cnt > 0:
                        cur.execute("""
                            SELECT
                                id,
                                subject AS ders,
                                topic AS konu,
                                difficulty,
                                question_text,
                                options,
                                correct_index,
                                explanation,
                                tags,
                                law_reference AS source
                            FROM questions
                            WHERE is_active = true
                            ORDER BY created_at;
                        """)

                        rows = cur.fetchall()

                        return [
                            {
                                "question_id": str(r[0]),
                                "ders": r[1],
                                "konu": r[2],
                                "difficulty": r[3],
                                "question": r[4],
                                "options": r[5],
                                "correct_answer": r[6],
                                "explanation": r[7],
                                "tags": r[8],
                                "source": r[9],
                            }
                            for r in rows
                        ]

    except Exception as e:
        print(f"[questions_repo] DB read failed. Error: {e}")

    return []
