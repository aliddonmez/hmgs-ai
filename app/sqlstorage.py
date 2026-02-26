# app/sqlstorage.py

import os
import sqlite3
from typing import List, Dict, Optional

from dotenv import load_dotenv

load_dotenv()

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "hmgs.db")


def _storage_backend() -> str:
    # Default sqlite => mevcut sistem aynı kalsın
    return (os.getenv("STORAGE_BACKEND") or "sqlite").strip().lower()


# -----------------------------
# SQLITE BACKEND (MEVCUT)
# -----------------------------
def _sqlite_get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def _sqlite_init_storage():
    with _sqlite_get_connection() as conn:
        conn.execute(
            """
        CREATE TABLE IF NOT EXISTS quiz_attempt_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attempt_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            question_id TEXT NOT NULL,
            ders TEXT,
            konu TEXT,
            selected_option INTEGER NOT NULL,
            correct_option INTEGER NOT NULL,
            is_correct INTEGER NOT NULL,
            confidence REAL,
            retrieval_score REAL
        );
        """
        )
        conn.execute(
            """
        CREATE INDEX IF NOT EXISTS idx_attempt_id
        ON quiz_attempt_answers (attempt_id);
        """
        )
        conn.execute(
            """
        CREATE INDEX IF NOT EXISTS idx_user_id
        ON quiz_attempt_answers (user_id);
        """
        )
        conn.commit()


def _sqlite_save_attempt_rows(rows: List[Dict]):
    if not rows:
        return

    _sqlite_init_storage()

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
        :attempt_id,
        :user_id,
        :timestamp,
        :question_id,
        :ders,
        :konu,
        :selected_option,
        :correct_option,
        :is_correct,
        :confidence,
        :retrieval_score
    );
    """
    with _sqlite_get_connection() as conn:
        conn.executemany(sql, rows)
        conn.commit()


def _sqlite_load_attempts(user_id: Optional[str] = None):
    with _sqlite_get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        if user_id:
            cur.execute("SELECT * FROM quiz_attempt_answers WHERE user_id = ?;", (user_id,))
        else:
            cur.execute("SELECT * FROM quiz_attempt_answers;")

        return [dict(row) for row in cur.fetchall()]


# -----------------------------
# POSTGRES BACKEND (HAZIR, AMA DEVREDE DEĞİL)
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
    import psycopg  # requirements.txt içinde var

    return psycopg.connect(**_pg_conn_info())


def _pg_init_storage():
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
            cur.execute("CREATE INDEX IF NOT EXISTS idx_attempt_id ON quiz_attempt_answers (attempt_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON quiz_attempt_answers (user_id);")
        conn.commit()


def _pg_save_attempt_rows(rows: List[Dict]):
    if not rows:
        return

    _pg_init_storage()

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


def _pg_load_attempts(user_id: Optional[str] = None):
    from psycopg.rows import dict_row

    _pg_init_storage()

    with _pg_get_connection() as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            if user_id:
                cur.execute("SELECT * FROM quiz_attempt_answers WHERE user_id = %s ORDER BY id;", (user_id,))
            else:
                cur.execute("SELECT * FROM quiz_attempt_answers ORDER BY id;")
            return cur.fetchall()


# -----------------------------
# PUBLIC API (UYGULAMA BUNU KULLANIYOR)
# -----------------------------
def init_storage():
    backend = _storage_backend()
    if backend == "postgres":
        return _pg_init_storage()
    return _sqlite_init_storage()


def save_attempt_rows(rows: List[Dict]):
    backend = _storage_backend()

    # Normal davranış
    if backend == "postgres":
        _pg_save_attempt_rows(rows)
    else:
        _sqlite_save_attempt_rows(rows)

    # Geçiş güvenliği: çift yazma (opsiyonel)
    if (os.getenv("DUAL_WRITE") or "").strip() == "1":
        try:
            # Hangi backend aktif olursa olsun, diğerine de yaz
            if backend == "postgres":
                _sqlite_save_attempt_rows(rows)
            else:
                _pg_save_attempt_rows(rows)
        except Exception as e:
            # Uygulama asla düşmesin: sadece log
            print(f"[DUAL_WRITE WARNING] Secondary write failed: {e}")


def load_attempts(user_id: Optional[str] = None):
    backend = _storage_backend()

    if backend == "postgres":
        try:
            return _pg_load_attempts(user_id=user_id)
        except Exception as e:
            print(f"[FALLBACK] Postgres read failed, using SQLite. Error: {e}")
            return _sqlite_load_attempts(user_id=user_id)

    # sqlite normal
    return _sqlite_load_attempts(user_id=user_id)