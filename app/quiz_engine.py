# app/quiz_engine.py
# -- QUIZ MOTORU (UI-dostu) --

from datetime import datetime, timezone


def start_quiz(
    question_pool, n_questions=20, mode="balanced", weak_topics=None, seed=None
):
    from app.question_select import select_questions

    selected = select_questions(
        question_pool, n_questions, mode=mode, weak_topics=weak_topics, seed=seed
    )

    return {
        "questions": selected,
        "current_index": 0,
        "score": 0,
        "answers": [],
        "attempt_id": str(uuid.uuid4()),
        "started_at": datetime.now(timezone.utc),
        "question_start_time": datetime.now(timezone.utc),
    }


def get_current_question(state):
    """
    Mevcut soruyu döndürür.
    Sorular bittiyse None döner.
    """
    idx = state["current_index"]
    questions = state["questions"]

    if idx >= len(questions):
        return None  # Quiz bitti
    return questions[idx]  # Şu anki soru


def submit_answer(state, user_answer_index):
    """
    Kullanıcının verdiği cevabı işler.
    Doğru/yanlış kontrolü yapar ve state'i günceller.
    """
    question = get_current_question(state)
    if question is None:
        return {"error": "Quiz bitmiş veya soru bulunamadı."}

    now = datetime.now(timezone.utc)
    response_time = (now - state["question_start_time"]).total_seconds()

    correct_index = question["correct_index"]
    is_correct = user_answer_index == correct_index

    # Doğruysa skoru artır
    if is_correct:
        state["score"] += 1

    # Cevabı logla (ileride analiz için)
    state["answers"].append(
        {
            "question_id": question["question_id"],
            "selected_option": user_answer_index,
            "correct_option": correct_index,
            "is_correct": is_correct,
            "confidence": question.get("confidence"),
            "retrieval_score": question.get("retrieval_score"),
            "response_time": response_time,
        }
    )

    # Bir sonraki soruya geç
    state["current_index"] += 1
    state["question_start_time"] = datetime.now(timezone.utc)
    # UI'ye döndürülecek sonuç
    return {
        "dogru_mu": is_correct,
        "selected_index": user_answer_index,
        "correct_index": correct_index,
        "aciklama": question.get("explanation"),
    }


def is_quiz_finished(state):
    """
    Quiz bitmiş mi kontrolü.
    """
    return state["current_index"] >= len(state["questions"])


# --- UI için kolay isimlendirme ---


def is_finished(state):
    """
    UI tarafında daha okunabilir isim.
    """
    return is_quiz_finished(state)


def get_score(state):
    """
    Skor ve toplam soru sayısını döndürür.
    UI için hazır format.
    """
    total = len(state["questions"])
    return {"score": state["score"], "total": total}


import uuid
from datetime import datetime

from datetime import datetime, timezone


def export_attempt_rows(state, user_id: str):
    """
    Quiz tamamlandıktan sonra SQL'e yazılacak satırları üretir.
    Her soru = 1 satır
    """

    attempt_id = state["attempt_id"]
    timestamp = datetime.now(timezone.utc)

    rows = []

    for ans in state["answers"]:
        rows.append(
            {
                "attempt_id": attempt_id,
                "user_id": user_id,
                "question_id": ans["question_id"],
                "selected_option": ans["selected_option"],
                "correct_option": ans["correct_option"],
                "is_correct": ans["is_correct"],
                "response_time_seconds": ans.get("response_time"),
                "answered_at": timestamp,
            }
        )

    return rows
