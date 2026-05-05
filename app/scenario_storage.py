# app/scenario_storage.py

import os
from typing import List, Dict, Optional
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

# .env dosyasındaki PostgreSQL bağlantı bilgilerini yükler
load_dotenv()

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

def init_scenario_storage():
    """
    Senaryo tablosunu oluşturur.
    """
    with _pg_get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS scenario_cases (
                    id SERIAL PRIMARY KEY,

                    title VARCHAR(255) NOT NULL,
                    course VARCHAR(100) NOT NULL DEFAULT 'Ceza Hukuku',
                    topic VARCHAR(150) NOT NULL,
                    subtopic VARCHAR(150),

                    difficulty VARCHAR(20) NOT NULL DEFAULT 'Orta',

                    source_court VARCHAR(255),
                    source_case_no VARCHAR(100),
                    source_decision_no VARCHAR(100),
                    source_date VARCHAR(50),
                    source_file_name VARCHAR(255),

                    scenario_text TEXT NOT NULL,
                    question_text TEXT NOT NULL,

                    option_a TEXT NOT NULL,
                    option_b TEXT NOT NULL,
                    option_c TEXT NOT NULL,
                    option_d TEXT NOT NULL,

                    correct_option CHAR(1) NOT NULL CHECK (correct_option IN ('A', 'B', 'C', 'D')),

                    explanation TEXT NOT NULL,
                    legal_basis TEXT,

                    is_active BOOLEAN DEFAULT TRUE,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        conn.commit()

def get_all_scenarios(limit: int = 50) -> List[Dict]:
    """
    Tüm aktif senaryoları getirir.
    """
    init_scenario_storage()
    with _pg_get_connection() as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM scenario_cases WHERE is_active = TRUE ORDER BY id DESC LIMIT %s", (limit,))
            return cur.fetchall()

def get_scenario_by_id(scenario_id: int) -> Optional[Dict]:
    """
    ID'ye göre tek bir senaryo getirir.
    """
    init_scenario_storage()
    with _pg_get_connection() as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM scenario_cases WHERE id = %s", (scenario_id,))
            return cur.fetchone()

def get_random_scenario() -> Optional[Dict]:
    """
    Rastgele bir senaryo getirir.
    """
    init_scenario_storage()
    with _pg_get_connection() as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM scenario_cases WHERE is_active = TRUE ORDER BY RANDOM() LIMIT 1")
            return cur.fetchone()
