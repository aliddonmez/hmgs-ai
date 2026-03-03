import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

SQLITE_PATH = os.path.join("data", "hmgs.db")

def read_sqlite_rows():
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM quiz_attempt_answers ORDER BY id;")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def write_postgres_rows(rows):
    import psycopg

    pg = psycopg.connect(
        host=os.getenv("PG_HOST", "localhost"),
        port=int(os.getenv("PG_PORT", "5432")),
        dbname=os.getenv("PG_DB", "postgres"),
        user=os.getenv("PG_USER", "postgres"),
        password=os.getenv("PG_PASSWORD", ""),
    )

    # Postgres tablosu var mı garanti
    with pg.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS quiz_attempt_answers (
            id BIGSERIAL PRIMARY KEY,
            attempt_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            question_id TEXT NOT NULL,
            ders TEXT,
            konu TEXT,
            selected_option INTEGER NOT NULL,
            correct_option INTEGER NOT NULL,
            is_correct INTEGER NOT NULL,
            confidence DOUBLE PRECISION,
            retrieval_score DOUBLE PRECISION
        );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_attempt_id ON quiz_attempt_answers (attempt_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON quiz_attempt_answers (user_id);")
    pg.commit()

    # Aynı kayıt tekrar taşınmasın diye basit dedup:
    # attempt_id + question_id + timestamp + user_id aynıysa yok say.
    existing = set()
    with pg.cursor() as cur:
        cur.execute("SELECT attempt_id, question_id, timestamp, user_id FROM quiz_attempt_answers;")
        for a, q, t, u in cur.fetchall():
            existing.add((a, q, t, u))

    to_insert = []
    for r in rows:
        key = (r["attempt_id"], r["question_id"], r["timestamp"], r["user_id"])
        if key in existing:
            continue
        to_insert.append({
            "attempt_id": r["attempt_id"],
            "user_id": r["user_id"],
            "timestamp": r["timestamp"],
            "question_id": r["question_id"],
            "ders": r.get("ders"),
            "konu": r.get("konu"),
            "selected_option": r["selected_option"],
            "correct_option": r["correct_option"],
            "is_correct": r["is_correct"],
            "confidence": r.get("confidence"),
            "retrieval_score": r.get("retrieval_score"),
        })

    if not to_insert:
        print("No new rows to insert (already migrated).")
        pg.close()
        return

    sql = """
    INSERT INTO quiz_attempt_answers (
        attempt_id, user_id, timestamp, question_id, ders, konu,
        selected_option, correct_option, is_correct, confidence, retrieval_score
    )
    VALUES (
        %(attempt_id)s, %(user_id)s, %(timestamp)s, %(question_id)s, %(ders)s, %(konu)s,
        %(selected_option)s, %(correct_option)s, %(is_correct)s, %(confidence)s, %(retrieval_score)s
    );
    """

    with pg.cursor() as cur:
        cur.executemany(sql, to_insert)
    pg.commit()
    pg.close()

    print(f"Migrated {len(to_insert)} rows to Postgres.")

if __name__ == "__main__":
    rows = read_sqlite_rows()
    print(f"Read {len(rows)} rows from SQLite.")
    write_postgres_rows(rows)