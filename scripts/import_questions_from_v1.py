import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import os
from dotenv import load_dotenv
import psycopg
from psycopg.types.json import Json

load_dotenv(dotenv_path=".env")

def pg_conn():
    return psycopg.connect(
        host=os.getenv("PG_HOST","localhost"),
        port=int(os.getenv("PG_PORT","5432")),
        dbname=os.getenv("PG_DB","postgres"),
        user=os.getenv("PG_USER","postgres"),
        password=os.getenv("PG_PASSWORD",""),
    )

def main():
    from data.questions_v1 import questions as qlist

    with pg_conn() as conn:
        with conn.cursor() as cur:
            for q in qlist:
                qid = q["id"]
                ders = q.get("dersadi")
                konu = q.get("konu")
                difficulty = q.get("zorluk")
                question_text = q.get("soru")
                options = q.get("secenekler")
                correct_index = q.get("dogru_cevap")
                explanation = q.get("aciklama")
                source = q.get("kaynak")

                if question_text is None or options is None or correct_index is None:
                    raise ValueError(f"Invalid question format for {qid}")

                # dogru_cevap zaten 0-based gibi (örnek: 1 => B)
                if not (0 <= int(correct_index) < len(options)):
                    raise ValueError(f"{qid}: correct_index out of range")

                cur.execute(
                    """
                    INSERT INTO questions (
                        id, ders, konu, difficulty, question_text, options,
                        correct_index, explanation, tags, source, version
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, 1
                    )
                    ON CONFLICT (id) DO UPDATE SET
                        ders = EXCLUDED.ders,
                        konu = EXCLUDED.konu,
                        difficulty = EXCLUDED.difficulty,
                        question_text = EXCLUDED.question_text,
                        options = EXCLUDED.options,
                        correct_index = EXCLUDED.correct_index,
                        explanation = EXCLUDED.explanation,
                        tags = EXCLUDED.tags,
                        source = EXCLUDED.source;
                    """,
                    (
                        qid,
                        ders,
                        konu,
                        difficulty,
                        question_text,
                        Json(options),
                        int(correct_index),
                        explanation,
                        None,
                        source,
                    ),
                )

        conn.commit()

    print(f"Imported/updated {len(qlist)} questions into Postgres.")

if __name__ == "__main__":
    main()