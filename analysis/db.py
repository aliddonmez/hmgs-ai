# analysis/db.py

import os
from dotenv import load_dotenv
import psycopg


load_dotenv()  # .env varsa otomatik yüklesin


def get_conn():
    """
    PostgreSQL bağlantısı döndürür.
    Ortam değişkenleri:
    PG_HOST, PG_PORT, PG_DB, PG_USER, PG_PASSWORD
    """
    return psycopg.connect(
        host=os.environ.get("PG_HOST", "localhost"),
        port=int(os.environ.get("PG_PORT", "5433")),
        dbname=os.environ.get("PG_DB", "postgres"),
        user=os.environ.get("PG_USER", "postgres"),
        password=os.environ.get("PG_PASSWORD", "1234"),
    )
