# analysis/cli_report.py

# app/streamlit_app.py
import sys
import os

# -------------------------------------------------
# Proje root'unu path'e ekle
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from app.sqlstorage import load_attempts
from analysis.quizanalysis import compute_topic_stats
from analysis.rank_topics import rank_weak_topics
from analysis.suggestions import generate_study_suggestions


def run_12_3():
    user_id = input("Kullanıcı ID: ").strip()

    if not user_id:
        print("❌ Kullanıcı ID boş olamaz.")
        return

    rows = load_attempts(user_id)

    if not rows:
        print(f"ℹ️ '{user_id}' için kayıt bulunamadı.")
        return

    topic_stats = compute_topic_stats(rows)
    ranked_topics = rank_weak_topics(topic_stats)
    suggestions = generate_study_suggestions(ranked_topics)

    print("\n📉 12.4 — Zayıflıktan Güçlüye Konu Sıralaması\n")

    for i, t in enumerate(ranked_topics, start=1):
        print(
            f"{i}. {t['konu']} | "
            f"%{t['accuracy']} | "
            f"{t['n_questions']} soru | "
            f"{t['data_status']}"
        )
    print("\n🧠 12.5 — Çalışma Önerileri\n")

    for s in suggestions:
        print(f"- {s}")


if __name__ == "__main__":
    run_12_3()
