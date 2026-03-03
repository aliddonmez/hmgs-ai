import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
import psycopg
from psycopg.types.json import Json

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

load_dotenv(dotenv_path=str(ROOT / ".env"))

def pg_conn():
    return psycopg.connect(
        host=os.getenv("PG_HOST","localhost"),
        port=int(os.getenv("PG_PORT","5432")),
        dbname=os.getenv("PG_DB","postgres"),
        user=os.getenv("PG_USER","postgres"),
        password=os.getenv("PG_PASSWORD",""),
    )

def validate(row: dict):
    required = ["id", "dersadi", "konu", "soru", "secenekler", "dogru_cevap"]
    for k in required:
        if k not in row:
            raise ValueError(f"Missing key: {k}")

    if not isinstance(row["secenekler"], list) or len(row["secenekler"]) < 2:
        raise ValueError("secenekler must be a list with at least 2 items")

    c = int(row["dogru_cevap"])
    if not (0 <= c < len(row["secenekler"])):
        raise ValueError("dogru_cevap out of range")

def main(path: str):
    inserted = 0
    updated = 0

    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.readlines() if ln.strip()]

    rows = [json.loads(ln) for ln in lines]
    for r in rows:
        validate(r)

    with pg_conn() as conn:
        with conn.cursor() as cur:
            for r in rows:
                qid = r["id"]
                ders = r.get("dersadi")
                konu = r.get("konu")
                difficulty = r.get("zorluk")
                question_text = r.get("soru")
                options = r.get("secenekler")
                correct_index = int(r.get("dogru_cevap"))
                explanation = r.get("aciklama")
                source = r.get("kaynak")
                tags = r.get("etiketler")

                cur.execute("SELECT 1 FROM questions WHERE id = %s;", (qid,))
                exists = cur.fetchone() is not None

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
                        correct_index,
                        explanation,
                        Json(tags) if tags is not None else None,
                        source,
                    ),
                )

                if exists:
                    updated += 1
                else:
                    inserted += 1

        conn.commit()

    print(f"Inserted: {inserted}, Updated: {updated}, Total processed: {len(rows)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/import_questions_jsonl.py data/imports/questions/<file>.jsonl")
        raise SystemExit(1)
    main(sys.argv[1])
