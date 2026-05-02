import sys
import os

# Proje root ekle
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from app.quiz_engine import (
    start_quiz,
    get_current_question,
    submit_answer,
    is_quiz_finished,
    export_attempt_rows,
)
from app.sqlstorage import (
    save_attempt_rows,
    create_quiz_attempt,
    finalize_quiz_attempt,
)

from app.repositories.questions_repo import get_questions
from app.question_select import select_questions


# ----------------------------
# SORULARI YÜKLE
# ----------------------------
questions = get_questions()

if not questions:
    print("❌ Soru bulunamadı.")
    sys.exit()


# ----------------------------
# QUIZ MODU SEÇ
# ----------------------------
print("Quiz Modu Seç:")
print("1 - Random (10 soru)")
print("2 - Balanced (20 soru)")
print("3 - Weak Focus (20 soru)")

secim = input("Seçim: ")

if secim == "1":
    selected = select_questions(questions, 10, mode="random")

elif secim == "2":
    selected = select_questions(questions, 20, mode="balanced")

elif secim == "3":
    konu = input("Zayıf konu gir: ")
    selected = select_questions(questions, 20, mode="weak_focus", weak_topics=[konu])
else:
    print("❌ Geçersiz seçim.")
    sys.exit()

if not selected:
    print("❌ Seçilen moda göre soru bulunamadı.")
    sys.exit()


# ----------------------------
# QUIZ BAŞLAT
# ----------------------------
quiz_state = start_quiz(selected)
create_quiz_attempt(
    attempt_id=quiz_state["attempt_id"],
    user_id="terminal_test",
    mode="balanced",
    total_questions=len(quiz_state["questions"]),
    started_at=quiz_state["started_at"],
)

# ----------------------------
# QUIZ LOOP
# ----------------------------
while not is_quiz_finished(quiz_state):
    q = get_current_question(quiz_state)

    print("\n❓", q["question"])
    for i, secenek in enumerate(q["options"]):
        print(f"{i}. {secenek}")

    try:
        answer = int(input("Cevabın: "))
    except ValueError:
        print("❌ Lütfen sayı gir.")
        continue

    result = submit_answer(quiz_state, answer)

    if "error" in result:
        print("❌", result["error"])
        continue

    if result["dogru_mu"]:
        print("✅ Doğru")
    else:
        print("❌ Yanlış")
        print("ℹ️", result["aciklama"])


# ----------------------------
# SONUÇ
# ----------------------------
print("\n🎉 Quiz bitti")
print("Skor:", quiz_state["score"], "/", len(quiz_state["questions"]))

rows = export_attempt_rows(quiz_state, user_id="terminal_test")

save_attempt_rows(rows)

from datetime import datetime, timezone

duration = (datetime.now(timezone.utc) - quiz_state["started_at"]).total_seconds()

finalize_quiz_attempt(
    attempt_id=quiz_state["attempt_id"],
    correct_count=quiz_state["score"],
    wrong_count=len(quiz_state["questions"]) - quiz_state["score"],
    finished_at=datetime.now(timezone.utc),
    total_duration_seconds=int(duration),
)
