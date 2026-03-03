import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)
from app.repositories.questions_repo import get_questions
questions = get_questions()
from app.quiz_engine import start_quiz, get_current_question, submit_answer, is_finished, get_score

def test_normal_flow():
    state = start_quiz(questions[:3])
    print("=== Day10 Integration Test: normal flow ===")
    print("Total:", get_score(state)["total"])

    while not is_finished(state):
        q = get_current_question(state)
        if q is None:
            raise RuntimeError("get_current_question None döndü ama quiz bitmemiş görünüyor")

        print(f"\nSoru {state['current_index']+1}: {q['soru']}")
        for i, opt in enumerate(q["secenekler"]):
            print(f"  {i}. {opt}")

        # Bilerek 0 seçiyoruz (doğru/yanlış olabilir)
        result = submit_answer(state, 0)

        if "error" in result:
            raise RuntimeError("Normal akışta error dönmemeliydi: " + result["error"])

        print("  dogru_mu:", result["dogru_mu"],
              "| selected:", result["selected_index"],
              "| correct:", result["correct_index"])
        print("  kaynak:", result["kaynak"])

    score = get_score(state)
    print("\nBitti. Skor:", score["score"], "/", score["total"])
    print("answers log size:", len(state["answers"]))
    print("=== OK ===")


def test_validation_guards():
    state = start_quiz(questions[:1])
    q = get_current_question(state)

    print("\n=== Day10 Integration Test: validation guards ===")
    # Aralık dışı
    r1 = submit_answer(state, 99)
    print("Out of range:", r1)

    # Tip hatası
    r2 = submit_answer(state, "A")
    print("Wrong type:", r2)

    # Valid cevapla ilerleyebiliyor mu?
    r3 = submit_answer(state, 0)
    print("Valid submit:", r3)

    print("Finished?:", is_finished(state))
    print("Score:", get_score(state))
    print("=== OK ===")


if __name__ == "__main__":
    test_normal_flow()
    test_validation_guards()
