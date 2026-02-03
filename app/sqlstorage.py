##app/sqlstorage.py

import sqlite3
from typing import List,Dict
import os 

DB_DIR="data"
DB_PATH=os.path.join(DB_DIR,"hmgs.db")

##YOKSA OLUŞTURUR VARSA BAĞLANIR
def get_connection():
    os.makedirs(DB_DIR,exist_ok=True)
    return sqlite3.connect(DB_PATH)

##db hazırlığı tablo oluşumu vb 
def init_storage():
    with get_connection() as conn:
        conn.execute("""
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
        """)
        conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_attempt_id
        ON quiz_attempt_answers (attempt_id);
        """)
        conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_user_id
        ON quiz_attempt_answers (user_id);
        """)
        conn.commit()


##quizde verilen cevapları kaydetme 
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
    ##değerler sonradan pythondan gelecek dolacak demek 
    with get_connection() as conn:
        conn.executemany(sql, rows)
        conn.commit()



##db kayıtları okuma 
def load_attempts(user_id: str | None = None):
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        if user_id:
            cur.execute(
                "SELECT * FROM quiz_attempt_answers WHERE user_id = ?;",
                (user_id,)
            )
        else:
            cur.execute("SELECT * FROM quiz_attempt_answers;")

        return [dict(row) for row in cur.fetchall()]        


