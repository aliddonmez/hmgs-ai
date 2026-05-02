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


def get_questions():
    with _pg_conn() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
            SELECT id, subject, topic, subtopic, difficulty,
            question_text, options, correct_index,
            explanation, tags, law_reference
            FROM questions
            WHERE is_active = true
            ORDER BY created_at DESC;
        """
            )

            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()

            sonuc = []

            for row in rows:
                data = dict(zip(columns, row))

                sonuc.append(
                    {
                        "question_id": str(data["id"]),
                        "subject": data["subject"],
                        "topic": data["topic"],
                        "subtopic": data["subtopic"],
                        "difficulty": data["difficulty"],
                        "question": data["question_text"],
                        "options": data["options"],
                        "correct_index": data["correct_index"],
                        "explanation": data["explanation"],
                        "tags": data["tags"],
                        "law_reference": data["law_reference"],
                    }
                )

            return sonuc
