import os
import sys
import json
import psycopg
from dotenv import load_dotenv
from google import genai

load_dotenv()


DB_NAME = os.getenv("PG_DB", "postgres")
DB_USER = os.getenv("PG_USER", "postgres")
DB_PASSWORD = os.getenv("PG_PASSWORD", "")
DB_HOST = os.getenv("PG_HOST", "localhost")
DB_PORT = os.getenv("PG_PORT", "5432")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def get_connection():
    return psycopg.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )


def get_tck_chunks(limit=3):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            id,
            document_id,
            chunk_index,
            content,
            meta
        FROM document_chunks
        WHERE document_id = 'tck'
          AND meta ->> 'chunk_type' = 'article'
        ORDER BY RANDOM()
        LIMIT %s;
    """,
        (limit,),
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


def build_prompt(chunk):
    chunk_id, document_id, chunk_index, content, meta = chunk

    kanun = meta.get("kanun", "TCK")
    madde_no = meta.get("madde_no", "")
    title = meta.get("title", "")
    full_heading = meta.get("full_heading", f"{kanun} Madde {madde_no}")

    return f"""
Sen HMGS sınavına yönelik hukuk test soruları hazırlayan uzman bir soru yazıcısısın.

Aşağıdaki kanun maddesine dayanarak 5 seçenekli, tek doğru cevaplı, özgün bir HMGS tarzı test sorusu üret.

Kesin kurallar:
- Soru sadece verilen kanun maddesine dayanmalı.
- ÖSYM sorularını kopyalama veya çok benzerini yazma.
- Soru özgün olmalı.
- Tek bir doğru cevap olmalı.
- 5 seçenek üret.
- Seçenekler kısa, açık ve sınav diline uygun olmalı.
- Çeldiriciler mantıklı olmalı ama doğru cevapla karıştırılmayacak kadar net ayrılmalı.
- Doğru cevap tartışmasız olmalı.
- Açıklama kısa, öğretici ve verilen maddeye bağlı olmalı.
- JSON dışında hiçbir metin yazma.
- Markdown kod bloğu kullanma.

Soru kalitesi:
- HMGS mantığına yakın olsun.
- Ezber + yorum karışımı olabilir.
- Gerekiyorsa “aşağıdakilerden hangisi doğrudur?” veya “hangisi yanlıştır?” tarzı kullanılabilir.
- Çok basit tanım sorusu olmasın; mümkünse madde bilgisini ölçsün.

Ders:
Ceza Hukuku

Kaynak:
{full_heading}

Madde başlığı:
{title}

Madde metni:
\"\"\"
{content}
\"\"\"

Cevabı sadece şu JSON formatında döndür:

{{
  "question_text": "...",
  "options": [
    "...",
    "...",
    "...",
    "...",
    "..."
  ],
  "correct_index": 0,
  "explanation": "...",
  "subject": "Ceza Hukuku",
  "topic": "{title}",
  "subtopic": "{full_heading}",
  "difficulty": 3,
  "question_type": "law_based",
  "tags": ["hmgs", "ceza_hukuku", "tck"]
}}
"""


def generate_question_with_gemini(prompt):
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY .env dosyasında bulunamadı.")

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

    return response.text


def clean_json_response(text):
    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1).strip()

    if text.startswith("```"):
        text = text.replace("```", "", 1).strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    return text


def validate_question(data):
    required_fields = [
        "question_text",
        "options",
        "correct_index",
        "explanation",
        "subject",
        "topic",
        "difficulty",
        "question_type",
    ]

    for field in required_fields:
        if field not in data:
            raise ValueError(f"Eksik alan: {field}")

    if not isinstance(data["options"], list):
        raise ValueError("options liste olmalı.")

    if len(data["options"]) != 5:
        raise ValueError("options tam olarak 5 seçenek içermeli.")

    if len(set(data["options"])) != 5:
        raise ValueError("Seçenekler birbirinden farklı olmalı.")

    if not isinstance(data["correct_index"], int):
        raise ValueError("correct_index sayı olmalı.")

    if data["correct_index"] < 0 or data["correct_index"] > 4:
        raise ValueError("correct_index 0 ile 4 arasında olmalı.")

    if len(data["question_text"].strip()) < 20:
        raise ValueError("question_text çok kısa.")

    if len(data["explanation"].strip()) < 20:
        raise ValueError("explanation çok kısa.")

    return True


def save_question(question_data, chunk):
    chunk_id, document_id, chunk_index, content, meta = chunk

    source_code = meta.get("source", document_id)
    law_name = meta.get("kanun", "TCK")
    article_number = meta.get("madde_no")
    title = meta.get("title")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO questions (
            question_text,
            options,
            correct_index,
            explanation,
            subject,
            topic,
            subtopic,
            difficulty,
            law_reference,
            tags,
            question_type,
            source_type,
            source_code,
            law_name,
            article_number,
            source_chunk_bigint_id,
            status,
            is_active
        )
        VALUES (
            %s, %s::jsonb, %s, %s,
            %s, %s, %s, %s,
            %s::jsonb, %s::jsonb,
            %s, %s, %s, %s, %s,
            %s, %s, true
        )
        RETURNING id;
    """,
        (
            question_data["question_text"],
            json.dumps(question_data["options"], ensure_ascii=False),
            question_data["correct_index"],
            question_data["explanation"],
            question_data["subject"],
            question_data.get("topic", title),
            question_data.get("subtopic"),
            question_data.get("difficulty", 3),
            json.dumps(meta, ensure_ascii=False),
            json.dumps(question_data.get("tags", []), ensure_ascii=False),
            question_data.get("question_type", "law_based"),
            "AI_GENERATED",
            source_code,
            law_name,
            article_number,
            chunk_id,
            "DRAFT",
        ),
    )

    question_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return question_id


def generate_questions(count=3):
    chunks = get_tck_chunks(limit=count)

    if not chunks:
        print("Kaynak chunk bulunamadı.")
        return

    print(f"Toplam seçilen kaynak madde: {len(chunks)}")

    success_count = 0

    for index, chunk in enumerate(chunks, start=1):
        chunk_id, document_id, chunk_index, content, meta = chunk

        print("\n" + "-" * 60)
        print(f"[{index}/{len(chunks)}] Soru üretiliyor")
        print(f"Kaynak: {meta.get('full_heading')}")
        print("-" * 60)

        try:
            prompt = build_prompt(chunk)
            raw_response = generate_question_with_gemini(prompt)
            cleaned_response = clean_json_response(raw_response)

            question_data = json.loads(cleaned_response)

            validate_question(question_data)

            question_id = save_question(question_data, chunk)

            success_count += 1

            print(f"Kaydedildi: {question_id}")
            print(f"Soru: {question_data['question_text']}")

        except Exception as e:
            print("Hata oluştu. Bu madde atlandı.")
            print(str(e))

    print("\nİşlem tamamlandı.")
    print(f"Başarılı kayıt: {success_count}/{len(chunks)}")


if __name__ == "__main__":
    count = 3

    if len(sys.argv) > 1:
        count = int(sys.argv[1])

    generate_questions(count)
