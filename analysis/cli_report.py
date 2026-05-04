# analysis/cli_report.py

import sys
import os

# -------------------------------------------------
# Proje root'unu Python path'e ekliyoruz.
# -------------------------------------------------
# Bu dosya analysis/ klasörü içinde olduğu için,
# doğrudan çalıştırıldığında Python bazen app/ veya analysis/
# içindeki diğer modülleri bulamayabilir.
#
# Örneğin:
# from analysis.user_report import get_user_report
#
# satırının çalışması için proje ana klasörünün sys.path içinde olması gerekir.
# Bu blok, proje ana dizinini otomatik olarak path'e ekler.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Kullanıcının performans raporunu üreten ana fonksiyon
from analysis.user_report import get_user_report


def run_report():
    """
    Terminal üzerinden kullanıcı performans raporu üretir.

    Akış:
    1. Kullanıcıdan user_id alınır.
    2. get_user_report() ile analiz raporu oluşturulur.
    3. Genel özet terminale yazdırılır.
    4. Veri yetersiz konular gösterilir.
    5. Zayıf konular gösterilir.
    6. Güçlü konular gösterilir.
    7. Çalışma önerileri gösterilir.
    """

    # Terminalden kullanıcı ID değeri alınır
    user_id = input("Kullanıcı ID: ").strip()

    # Boş user_id girilirse işlem durdurulur
    if not user_id:
        print("❌ Kullanıcı ID boş olamaz.")
        return

    # Kullanıcı için performans raporu oluşturulur.
    # min_n=3:
    # Bir konuda sağlıklı analiz yapılabilmesi için
    # en az 3 soru çözülmüş olmasını ister.
    report = get_user_report(user_id, min_n=3)

    # Rapor boş dönerse veri bulunamadı mesajı gösterilir
    if not report:
        print("⚠️ Veri bulunamadı.")
        return

    # Genel özet bilgileri alınır
    summary = report.get("summary", {})

    # -------------------------
    # GENEL ÖZET
    # -------------------------
    # Kullanıcının toplam soru, doğru, yanlış ve başarı oranı bilgileri yazdırılır.
    print("\n📊 GENEL ÖZET\n")
    print(f"Toplam soru : {summary.get('total_questions', 0)}")
    print(f"Doğru       : {summary.get('correct', 0)}")
    print(f"Yanlış      : {summary.get('wrong', 0)}")
    print(f"Doğruluk    : %{summary.get('accuracy', 0)}")

    # -------------------------
    # VERİ YETERSİZ KONULAR
    # -------------------------
    # Bir konuda yeterli soru çözülmediyse sistem o konu için
    # güvenilir analiz yapmaz. Bu konular burada listelenir.
    insufficient = report.get("insufficient_data_topics", [])

    if insufficient:
        print("\n⚠️ VERİ YETERSİZ KONULAR\n")

        # Her veri yetersiz konu için açıklama mesajı yazdırılır
        for t in insufficient:
            print(f"- {t.get('message', '')}")

    # -------------------------
    # ZAYIF KONULAR
    # -------------------------
    # Başarı oranı belirlenen eşiğin altında olan konular listelenir.
    # Bu eşik user_report.py içinde belirleniyor.
    weak_topics = report.get("weak_topics", [])

    if weak_topics:
        print("\n📉 ZAYIF KONULAR\n")

        # Zayıf konular numaralı şekilde yazdırılır
        for i, t in enumerate(weak_topics, start=1):
            print(
                f"{i}. {t.get('konu')} | "
                f"%{t.get('accuracy')} | "
                f"{t.get('n_questions')} soru"
            )

    # -------------------------
    # GÜÇLÜ KONULAR
    # -------------------------
    # Başarı oranı iyi olan konular listelenir.
    strong_topics = report.get("strong_topics", [])

    if strong_topics:
        print("\n💪 GÜÇLÜ KONULAR\n")

        # Güçlü konular madde madde yazdırılır
        for t in strong_topics:
            print(
                f"- {t.get('konu')} | "
                f"%{t.get('accuracy')} | "
                f"{t.get('n_questions')} soru"
            )

    # -------------------------
    # ÖNERİLER
    # -------------------------
    # suggestions.py tarafından üretilen statik/kural tabanlı öneriler yazdırılır.
    suggestions = report.get("suggestions", [])

    if suggestions:
        print("\n🧠 ÇALIŞMA ÖNERİLERİ\n")

        # Her öneri ayrı satır olarak yazdırılır
        for s in suggestions:
            print(f"- {s}")


# Bu dosya doğrudan çalıştırılırsa run_report() fonksiyonu çağrılır.
# Örnek:
# python analysis/cli_report.py
if __name__ == "__main__":
    run_report()