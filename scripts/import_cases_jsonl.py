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
    required = ["id", "dersadi", "konu", "baslik", "vaka_metni"]
    for k in required:
        if k not in row:
            raise ValueError(f"Missing key: {k}")

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
                cid = r["id"]
                ders = r.get("dersadi")
                konu = r.get("konu")
                title = r.get("baslik")
                case_text = r.get("vaka_metni")
                tags = r.get("etiketler")
                source = r.get("kaynak")

                cur.execute("SELECT 1 FROM cases WHERE id = %s;", (cid,))
                exists = cur.fetchone() is not None

                cur.execute(
                    """
                    INSERT INTO cases (
                        id, ders, konu, title, case_text, tags, source, version
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s, %s, 1
                    )
                    ON CONFLICT (id) DO UPDATE SET
                        ders = EXCLUDED.ders,
                        konu = EXCLUDED.konu,
                        title = EXCLUDED.title,
                        case_text = EXCLUDED.case_text,
                        tags = EXCLUDED.tags,
                        source = EXCLUDED.source;
                    """,
                    (
                        cid, ders, konu, title, case_text,
                        Json(tags) if tags is not None else None,
                        source
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
        print("Usage: python scripts/import_cases_jsonl.py data/imports/cases/<file>.jsonl")
        raise SystemExit(1)
    main(sys.argv[1])
