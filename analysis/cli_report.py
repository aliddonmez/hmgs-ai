# analysis/cli_report.py

import sys
import os

# -------------------------------------------------
# Proje root'unu path'e ekle
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from analysis.user_report import get_user_report


def run_report():
    user_id = input("Kullanıcı ID: ").strip()

    if not user_id:
        print("❌ Kullanıcı ID boş olamaz.")
        return

    report = get_user_report(user_id, min_n=3)
    summary = report["summary"]

    # -------------------------
    # GENEL ÖZET
    # -------------------------
    print("\n📊 GENEL ÖZET\n")
    print(f"Toplam soru : {summary['total_questions']}")
    print(f"Doğru       : {summary['correct']}")
    print(f"Yanlış      : {summary['wrong']}")
    print(f"Doğruluk    : %{summary['accuracy']}")

    # -------------------------
    # VERİ YETERSİZ KONULAR
    # -------------------------
    if report["insufficient_data_topics"]:
        print("\n⚠️ VERİ YETERSİZ KONULAR\n")
        for t in report["insufficient_data_topics"]:
            print(f"- {t['message']}")

    # -------------------------
    # ZAYIF KONULAR
    # -------------------------
    if report["weak_topics"]:
        print("\n📉 ZAYIF KONULAR\n")
        for i, t in enumerate(report["weak_topics"], start=1):
            print(
                f"{i}. {t['konu']} | " f"%{t['accuracy']} | " f"{t['n_questions']} soru"
            )

    # -------------------------
    # GÜÇLÜ KONULAR
    # -------------------------
    if report["strong_topics"]:
        print("\n💪 GÜÇLÜ KONULAR\n")
        for t in report["strong_topics"]:
            print(f"- {t['konu']} | " f"%{t['accuracy']} | " f"{t['n_questions']} soru")

    # -------------------------
    # ÖNERİLER
    # -------------------------
    if report["suggestions"]:
        print("\n🧠 ÇALIŞMA ÖNERİLERİ\n")
        for s in report["suggestions"]:
            print(f"- {s}")


if __name__ == "__main__":
    run_report()
