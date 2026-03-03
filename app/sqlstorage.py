import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row

load_dotenv()


# -----------------------------
# POSTGRES CONNECTION
# -----------------------------
def _pg_conn_info():
    return {
        "host": os.getenv("PG_HOST", "localhost"),
        "port": int(os.getenv("PG_PORT", "5432")),
        "dbname": os.getenv("PG_DB", "postgres"),
        "user": os.getenv("PG_USER", "postgres"),
        "password": os.getenv("PG_PASSWORD", ""),
    }


def _pg_get_connection():
    return psycopg.connect(**_pg_conn_info())


# -----------------------------
# STORAGE INIT
# -----------------------------
def init_storage():
    with _pg_get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
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
            """
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_attempt_id ON quiz_attempt_answers (attempt_id);"
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_user_id ON quiz_attempt_answers (user_id);"
            )
        conn.commit()


# -----------------------------
# SAVE
# -----------------------------
def save_attempt_rows(rows: List[Dict]):
    if not rows:
        return

    init_storage()

    sql = """
    INSERT INTO quiz_attempt_answers (
        attempt_id,
        user_id,
        timestamp,
        question_id,
        ders,
        konu,
        selected_option,
        correct_option,
        is_correct,
        confidence,
        retrieval_score
    )
    VALUES (
        %(attempt_id)s,
        %(user_id)s,
        %(timestamp)s,
        %(question_id)s,
        %(ders)s,
        %(konu)s,
        %(selected_option)s,
        %(correct_option)s,
        %(is_correct)s,
        %(confidence)s,
        %(retrieval_score)s
    );
    """

    with _pg_get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(sql, rows)
        conn.commit()


# -----------------------------
# LOAD
# -----------------------------
def load_attempts(user_id: Optional[str] = None):
    init_storage()

    with _pg_get_connection() as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            if user_id:
                cur.execute(
                    "SELECT * FROM quiz_attempt_answers WHERE user_id = %s ORDER BY id;",
                    (user_id,),
                )
            else:
                cur.execute("SELECT * FROM quiz_attempt_answers ORDER BY id;")
            return cur.fetchall()
