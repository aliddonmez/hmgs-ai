# analysis/cli_report.py

import sys
import os

# -------------------------------------------------
# Proje root'unu path'e ekle
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from analysis.user_report import get_user_report


def run_report():
    user_id = input("Kullanıcı ID: ").strip()

    if not user_id:
        print("❌ Kullanıcı ID boş olamaz.")
        return

    report = get_user_report(user_id, min_n=3)

    if not report:
        print("⚠️ Veri bulunamadı.")
        return

    summary = report.get("summary", {})

    # -------------------------
    # GENEL ÖZET
    # -------------------------
    print("\n📊 GENEL ÖZET\n")
    print(f"Toplam soru : {summary.get('total_questions', 0)}")
    print(f"Doğru       : {summary.get('correct', 0)}")
    print(f"Yanlış      : {summary.get('wrong', 0)}")
    print(f"Doğruluk    : %{summary.get('accuracy', 0)}")

    # -------------------------
    # VERİ YETERSİZ KONULAR
    # -------------------------
    insufficient = report.get("insufficient_data_topics", [])
    if insufficient:
        print("\n⚠️ VERİ YETERSİZ KONULAR\n")
        for t in insufficient:
            print(f"- {t.get('message','')}")

    # -------------------------
    # ZAYIF KONULAR
    # -------------------------
    weak_topics = report.get("weak_topics", [])
    if weak_topics:
        print("\n📉 ZAYIF KONULAR\n")
        for i, t in enumerate(weak_topics, start=1):
            print(
                f"{i}. {t.get('konu')} | "
                f"%{t.get('accuracy')} | "
                f"{t.get('n_questions')} soru"
            )

    # -------------------------
    # GÜÇLÜ KONULAR
    # -------------------------
    strong_topics = report.get("strong_topics", [])
    if strong_topics:
        print("\n💪 GÜÇLÜ KONULAR\n")
        for t in strong_topics:
            print(
                f"- {t.get('konu')} | "
                f"%{t.get('accuracy')} | "
                f"{t.get('n_questions')} soru"
            )

    # -------------------------
    # ÖNERİLER
    # -------------------------
    suggestions = report.get("suggestions", [])
    if suggestions:
        print("\n🧠 ÇALIŞMA ÖNERİLERİ\n")
        for s in suggestions:
            print(f"- {s}")


if __name__ == "__main__":
    run_report()
