from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB bağlantısı
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        port="5433",
        database="postgres",
        user="postgres",
        password="1234"  # burayı değiştir
    )

# 1. Tüm senaryoları getir
@app.get("/api/scenarios")
def get_scenarios():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM scenario_cases ORDER BY id;")
    scenarios = cur.fetchall()

    cur.close()
    conn.close()

    return scenarios


# 2. Tek senaryo getir
@app.get("/api/scenarios/{scenario_id}")
def get_scenario(scenario_id: int):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        "SELECT * FROM scenario_cases WHERE id = %s;",
        (scenario_id,)
    )
    scenario = cur.fetchone()

    cur.close()
    conn.close()

    return scenario


# 3. Yeni senaryo ekle
@app.post("/api/scenarios")
def create_scenario(scenario: dict):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO scenario_cases (
            title, course, topic, subtopic, difficulty,
            scenario_text, question_text,
            option_a, option_b, option_c, option_d,
            correct_option, explanation
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        scenario["title"],
        scenario["course"],
        scenario["topic"],
        scenario["subtopic"],
        scenario["difficulty"],
        scenario["scenario_text"],
        scenario["question_text"],
        scenario["option_a"],
        scenario["option_b"],
        scenario["option_c"],
        scenario["option_d"],
        scenario["correct_option"],
        scenario["explanation"]
    ))

    conn.commit()

    cur.close()
    conn.close()

    return {"message": "Scenario created successfully"}