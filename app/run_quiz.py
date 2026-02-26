
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from app.quiz_engine import (
    start_quiz,
    get_current_question,
    submit_answer,
    is_quiz_finished
)


from app.repositories.questions_repo import get_questions
questions = get_questions()


quiz_state = start_quiz(questions)

while not is_quiz_finished(quiz_state):
    q = get_current_question(quiz_state)

    print("\n❓", q["question"])
    for i, secenek in enumerate(q["options"]):
        print(f"{i}. {secenek}")

    answer = int(input("Cevabın: "))
    result = submit_answer(quiz_state, answer)

    if result["dogru_mu"]:
        print("✅ Doğru")
    else:
        print("❌ Yanlış")
        print("ℹ️", result["aciklama"])


from app.quiz_engine import export_attempt_rows
from app.sqlstorage import save_attempt_rows

print("\n🎉 Quiz bitti")
print("Skor:", quiz_state["score"])

rows = export_attempt_rows(
    quiz_state,
    user_id="terminal_test"
)

save_attempt_rows(rows)

print("💾 Quiz sonuçları veritabanına kaydedildi")

