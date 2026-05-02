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
# CREATE QUIZ ATTEMPT
# -----------------------------
def create_quiz_attempt(
    attempt_id: str, user_id: str, mode: str, total_questions: int, started_at
):
    sql = """
    INSERT INTO quiz_attempts(
        id,
        user_id,
        mode,
        total_questions,
        started_at
    )
    VALUES(
        %(id)s,
        %(user_id)s,
        %(mode)s,
        %(total_questions)s,
        %(started_at)s
    );
    """

    payload = {
        "id": attempt_id,
        "user_id": user_id,
        "mode": mode,
        "total_questions": total_questions,
        "started_at": started_at,
    }

    with _pg_get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, payload)
        conn.commit()


# -----------------------------
# SAVE ANSWERS
# -----------------------------
def save_attempt_rows(rows: List[Dict]):
    if not rows:
        return

    sql = """
    INSERT INTO quiz_attempt_answers (
        attempt_id,
        question_id,
        user_id,
        selected_option,
        correct_option,
        is_correct,
        response_time_seconds,
        answered_at
    )
    VALUES (
        %(attempt_id)s,
        %(question_id)s,
        %(user_id)s,
        %(selected_option)s,
        %(correct_option)s,
        %(is_correct)s,
        %(response_time_seconds)s,
        %(answered_at)s
    );
    """

    with _pg_get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(sql, rows)
        conn.commit()


# -----------------------------
# FINALIZE ATTEMPT
# -----------------------------
def finalize_quiz_attempt(
    attempt_id: str,
    correct_count: int,
    wrong_count: int,
    finished_at,
    total_duration_seconds: int,
):
    sql = """
    UPDATE quiz_attempts
    SET
        correct_count = %(correct_count)s,
        wrong_count = %(wrong_count)s,
        finished_at = %(finished_at)s,
        total_duration_seconds = %(total_duration_seconds)s
    WHERE id = %(attempt_id)s;
    """

    payload = {
        "attempt_id": attempt_id,
        "correct_count": correct_count,
        "wrong_count": wrong_count,
        "finished_at": finished_at,
        "total_duration_seconds": total_duration_seconds,
    }

    with _pg_get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, payload)
        conn.commit()


# -----------------------------
# LOAD (🔥 EN KRİTİK KISIM)
# -----------------------------
def load_attempt_answers(user_id: Optional[str] = None):
    with _pg_get_connection() as conn:
        conn.row_factory = dict_row

        with conn.cursor() as cur:

            if user_id:
                cur.execute(
                    """
                    SELECT 
                        a.*,
                        q.topic
                    FROM quiz_attempt_answers a
                    JOIN questions q ON a.question_id = q.id
                    WHERE a.user_id = %s
                    ORDER BY a.id;
                    """,
                    (user_id,),
                )
            else:
                cur.execute(
                    """
                    SELECT 
                        a.*,
                        q.topic
                    FROM quiz_attempt_answers a
                    JOIN questions q ON a.question_id = q.id
                    ORDER BY a.id;
                    """
                )

            return cur.fetchall()
