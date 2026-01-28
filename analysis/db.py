# analysis/db.py

import os
from dotenv import load_dotenv
import psycopg


load_dotenv() 
# .env varsa otomatik yüklesin
# Böylece credential'lar(şifre vb) koda gömülmez 

## Hangi veri kaynağından veri cekiyorum ? 
##DB bağlantısı tek noktadan yönetilir

def get_conn():
    return psycopg.connect(
        host=os.environ.get("PG_HOST", "localhost"),
        port=int(os.environ.get("PG_PORT", "5432")),
        dbname=os.environ.get("PG_DB", "postgres"),
        user=os.environ.get("PG_USER", "postgres"),
        password=os.environ.get("PG_PASSWORD", "1234"),
    )
