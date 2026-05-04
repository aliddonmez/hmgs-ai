# app/sqlstorage.py

import os
from typing import List, Dict, Optional

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

# .env dosyasındaki PostgreSQL bağlantı bilgilerini yükler
load_dotenv()


# -----------------------------
# POSTGRES CONNECTION
# -----------------------------

def _pg_conn_info():
    """
    PostgreSQL bağlantı bilgilerini .env dosyasından okur.

    Beklenen .env değişkenleri:
    PG_HOST
    PG_PORT
    PG_DB
    PG_USER
    PG_PASSWORD

    Eğer .env içinde değer yoksa varsayılan değerler kullanılır.
    """

    return {
        "host": os.getenv("PG_HOST", "localhost"),
        "port": int(os.getenv("PG_PORT", "5432")),
        "dbname": os.getenv("PG_DB", "postgres"),
        "user": os.getenv("PG_USER", "postgres"),
        "password": os.getenv("PG_PASSWORD", ""),
    }


def _pg_get_connection():
    """
    PostgreSQL veritabanı bağlantısı oluşturur.

    Bu fonksiyon diğer kayıt ve okuma işlemlerinde kullanılır.
    """

    return psycopg.connect(**_pg_conn_info())


# -----------------------------
# STORAGE INIT
# -----------------------------

def init_storage():
    """
    Quiz cevap kayıtlarının tutulacağı tabloyu oluşturur.

    Bu tablo, kullanıcının bir quiz sırasında verdiği cevapları saklar.

    Tablo:
    quiz_attempt_answers

    Alanlar:
    - attempt_id: Quiz oturumunu temsil eder
    - question_id: Çözülen sorunun ID değeri
    - user_id: Kullanıcı ID değeri
    - selected_option: Kullanıcının seçtiği şık indexi
    - correct_option: Doğru şık indexi
    - is_correct: Cevap doğru mu?
    - response_time_seconds: Kullanıcının cevaplama süresi
    - answered_at: Cevaplama zamanı
    """

    with _pg_get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS quiz_attempt_answers (
                    id BIGSERIAL PRIMARY KEY,
                    attempt_id UUID NOT NULL,
                    question_id UUID NOT NULL,
                    user_id TEXT NOT NULL,
                    selected_option INTEGER NOT NULL,
                    correct_option INTEGER NOT NULL,
                    is_correct BOOLEAN NOT NULL,
                    response_time_seconds DOUBLE PRECISION,
                    answered_at TIMESTAMP WITH TIME ZONE DEFAULT now()
                );
                """
            )

            # attempt_id üzerinden hızlı sorgu yapabilmek için index oluşturulur
            cur.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_attempt_id
                ON quiz_attempt_answers (attempt_id);
                """
            )

            # user_id üzerinden kullanıcı bazlı analiz yapılacağı için index oluşturulur
            cur.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_user_id
                ON quiz_attempt_answers (user_id);
                """
            )

            # question_id üzerinden questions tablosuyla JOIN yapılacağı için index faydalıdır
            cur.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_quiz_attempt_question_id
                ON quiz_attempt_answers (question_id);
                """
            )

        conn.commit()


# -----------------------------
# SAVE
# -----------------------------

def save_attempt_rows(rows: List[Dict]):
    """
    Kullanıcının quiz cevaplarını veritabanına kaydeder.

    Parametre:
    rows:
        Kaydedilecek cevap satırları listesi.

    Beklenen örnek veri:
    [
        {
            "attempt_id": "...",
            "question_id": "...",
            "user_id": "demo_user",
            "selected_option": 1,
            "correct_option": 2,
            "is_correct": False,
            "response_time_seconds": 12.5,
            "timestamp": "2026-05-03T21:30:00"
        }
    ]
    """

    # Boş liste geldiyse hiçbir şey yapma
    if not rows:
        return

    # Tablo yoksa oluşturulur
    init_storage()

    # Gelen veriler veritabanına uygun formata normalize edilir
    normalized_rows = []

    for r in rows:
        normalized_rows.append(
            {
                "attempt_id": r.get("attempt_id"),
                "question_id": r.get("question_id"),
                "user_id": r.get("user_id"),
                "selected_option": r.get("selected_option"),
                "correct_option": r.get("correct_option"),

                # is_correct değeri bool tipe çevrilir
                "is_correct": bool(r.get("is_correct")),

                "response_time_seconds": r.get("response_time_seconds"),

                # timestamp yoksa SQL tarafında now() kullanılacak
                "answered_at": r.get("timestamp"),
            }
        )

    # Cevap kayıtlarını tabloya ekleyen SQL
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
        COALESCE(%(answered_at)s::timestamptz, now())
    );
    """

    # executemany ile birden fazla cevap tek seferde kaydedilir
    with _pg_get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(sql, normalized_rows)

        conn.commit()


# -----------------------------
# LOAD
# -----------------------------

def load_attempts(user_id: Optional[str] = None):
    """
    Kullanıcının quiz cevap geçmişini veritabanından getirir.

    Bu fonksiyon performans analizi için kullanılır.

    Önemli:
    analysis/quizanalysis.py dosyası "konu" alanını bekliyor.
    Bu yüzden burada quiz_attempt_answers tablosu questions tablosuyla JOIN edilir
    ve q.topic değeri "konu" adıyla döndürülür.

    Dashboard, quiz ekranının çözdürdüğü aktif soru kümesiyle aynı kayıtları
    saymalıdır. Bu yüzden aktif soruların denemeleri analize dahil edilir.
    """

    # Tablo yoksa oluşturulur
    init_storage()

    with _pg_get_connection() as conn:
        # Sonuçları tuple yerine dict olarak almak için kullanılır
        conn.row_factory = dict_row

        with conn.cursor() as cur:

            # Belirli bir kullanıcı için cevap geçmişi getirilecekse
            if user_id:
                cur.execute(
                    """
                    SELECT
                        qa.id,
                        qa.attempt_id,
                        qa.question_id,
                        qa.user_id,
                        qa.selected_option,
                        qa.correct_option,
                        qa.is_correct,
                        qa.response_time_seconds,
                        qa.answered_at AS timestamp,

                        -- Performans analizi için gerekli konu bilgisi
                        q.topic AS konu,

                        -- Ek analizlerde kullanılabilecek diğer soru bilgileri
                        q.subject,
                        q.topic,
                        q.subtopic,
                        q.difficulty,
                        q.law_name,
                        q.article_number
                    FROM quiz_attempt_answers qa
                    JOIN questions q ON q.id = qa.question_id
                    WHERE qa.user_id = %s
                      AND q.is_active = true
                    ORDER BY qa.id;
                    """,
                    (user_id,),
                )

            # user_id verilmezse tüm kullanıcıların cevap geçmişi getirilir
            else:
                cur.execute(
                    """
                    SELECT
                        qa.id,
                        qa.attempt_id,
                        qa.question_id,
                        qa.user_id,
                        qa.selected_option,
                        qa.correct_option,
                        qa.is_correct,
                        qa.response_time_seconds,
                        qa.answered_at AS timestamp,

                        -- Performans analizi için gerekli konu bilgisi
                        q.topic AS konu,

                        -- Ek analizlerde kullanılabilecek diğer soru bilgileri
                        q.subject,
                        q.topic,
                        q.subtopic,
                        q.difficulty,
                        q.law_name,
                        q.article_number
                    FROM quiz_attempt_answers qa
                    JOIN questions q ON q.id = qa.question_id
                    WHERE q.is_active = true
                    ORDER BY qa.id;
                    """
                )

            # Dict listesi döndürülür
            return cur.fetchall()
