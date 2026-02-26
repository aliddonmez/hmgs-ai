import sys
import os

# Proje ana klasörünü (root) Python'ın import yoluna ekler
# Böylece data/ ve app/ klasörlerinden import yapabiliriz
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

# Soru listesi ve quiz motoru fonksiyonlarını içeri al
from app.repositories.questions_repo import get_questions
questions = get_questions()
from app.quiz_engine import (
    start_quiz,
    get_current_question,
    submit_answer,
    is_finished,
    get_score
)

def main():
    # Quiz'i başlat (başlangıç state'i oluşturulur)
    quiz = start_quiz(questions)

    # Kullanıcıya bilgilendirme
    print("\n=== MANUEL QUIZ TEST ===")
    print("Cevaplamak için 0-4 arası sayı gir.")
    print("Çıkmak için: q\n")

    # Quiz bitene kadar devam et
    while not is_finished(quiz):
        # Mevcut soruyu al
        q = get_current_question(quiz)

        # Soru başlığı ve ilerleme bilgisi
        print("----------------------------")
        print(f"Soru {quiz['current_index'] + 1}/{get_score(quiz)['total']}")
        print(q["soru"])
        print()

        # Şıkları ekrana yazdır
        for i, opt in enumerate(q["secenekler"]):
            print(f"{i}: {opt}")

        # Kullanıcıdan cevap al
        user_input = input("\nCevabın: ").strip()

        # Kullanıcı çıkmak isterse
        if user_input.lower() == "q":
            print("Quiz yarıda bırakıldı.")
            return

        # Sayıya çevrilemeyen girişleri engelle
        try:
            user_index = int(user_input)
        except ValueError:
            print("⚠️ Hatalı giriş. Lütfen sayı gir.")
            continue  # Aynı soruda kal

        # Cevabı quiz motoruna gönder
        result = submit_answer(quiz, user_index)

        # Motor hata döndürürse (aralık dışı vs.)
        if "error" in result:
            print("⚠️", result["error"])
            continue  # Aynı soruda kal

        # Doğru / yanlış geri bildirimi
        if result["dogru_mu"]:
            print("✅ Doğru")
        else:
            print("❌ Yanlış")
            print("ℹ️", result["aciklama"])  # Açıklama sadece yanlışta

        print()  # Görsel boşluk

    # Quiz bittikten sonra skor göster
    score = get_score(quiz)
    print("\n🎉 Quiz bitti")
    print("Skor:", score["score"], "/", score["total"])

# Dosya doğrudan çalıştırıldığında main fonksiyonunu başlat
if __name__ == "__main__":
    main()