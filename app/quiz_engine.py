# app/quiz_engine.py
# -- QUIZ MOTORU (UI-dostu) --

def start_quiz(questions):
    """
    Quiz başlatılırken çağrılır.
    Başlangıç state'ini oluşturur.
    """
    return {
        "questions": questions,      # Tüm soru listesi
        "current_index": 0,          # Şu an hangi sorudayız
        "score": 0,                  # Doğru sayısı
        "answers": []                # Kullanıcının verdiği cevaplar (log)
    }


def get_current_question(state):
    """
    Mevcut soruyu döndürür.
    Sorular bittiyse None döner.
    """
    idx = state["current_index"]
    questions = state["questions"]

    if idx >= len(questions):
        return None                  # Quiz bitti
    return questions[idx]            # Şu anki soru


def submit_answer(state, user_answer_index):
    """
    Kullanıcının verdiği cevabı işler.
    Doğru/yanlış kontrolü yapar ve state'i günceller.
    """
    question = get_current_question(state)
    if question is None:
        return {"error": "Quiz bitmiş veya soru bulunamadı."}

    options = question.get("secenekler", [])

    # Cevap integer değilse hata ver
    if not isinstance(user_answer_index, int):
        return {"error": "Cevap formatı hatalı. Sayı (int) olmalı."}

    # Cevap aralık dışıysa hata ver
    if user_answer_index < 0 or user_answer_index >= len(options):
        return {"error": f"Geçersiz seçim. 0-{len(options)-1} arası bir değer girin."}

    correct_index = question["dogru_cevap"]
    is_correct = (user_answer_index == correct_index)

    # Doğruysa skoru artır
    if is_correct:
        state["score"] += 1

    # Cevabı logla (ileride analiz için)
    state["answers"].append({
        "question_id": question["id"],
        "selected": user_answer_index,
        "correct": is_correct,
        "zorluk": question.get("zorluk")
    })

    # Bir sonraki soruya geç
    state["current_index"] += 1

    # UI'ye döndürülecek sonuç
    return {
        "dogru_mu": is_correct,
        "selected_index": user_answer_index,
        "correct_index": correct_index,
        "aciklama": question.get("aciklama"),
        "kaynak": question.get("kaynak")
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
    return {
        "score": state["score"],
        "total": total
    }