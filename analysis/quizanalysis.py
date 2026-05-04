# analysis/quizanalysis.py

from collections import defaultdict
from typing import List, Dict


def compute_topic_stats(attempt_rows: List[Dict], min_n: int = 3) -> List[Dict]:
    """
    Kullanıcının soru çözme geçmişinden konu bazlı istatistik üretir.

    Bu fonksiyon sadece TEK bir kullanıcıya ait attempt kayıtlarıyla çalışmalıdır.

    Parametreler:
    attempt_rows:
        Kullanıcının çözüm kayıtları listesi.

        Beklenen örnek veri:
        [
            {
                "konu": "Ceza Hukuku",
                "is_correct": True
            },
            {
                "konu": "Ceza Hukuku",
                "is_correct": False
            }
        ]

    min_n:
        Bir konu için sağlıklı analiz yapılabilmesi adına
        gereken minimum çözülmüş soru sayısı.

        Örnek:
        min_n = 3 ise kullanıcı bir konuda 1 veya 2 soru çözdüyse
        bu konu "yetersiz" kabul edilir.

    Dönen değer:
        Her konu için istatistik listesi döner.

        Örnek:
        [
            {
                "konu": "Ceza Hukuku",
                "n_questions": 10,
                "n_correct": 6,
                "n_wrong": 4,
                "accuracy": 60.0,
                "data_status": "yeterli"
            }
        ]
    """

    # Her konunun doğru/yanlış sonuçlarını tutmak için sözlük oluşturulur.
    #
    # defaultdict(list) sayesinde yeni bir konu geldiğinde
    # otomatik olarak boş liste oluşturulur.
    #
    # Örnek yapı:
    # {
    #   "Ceza Hukuku": [True, False, True],
    #   "Medeni Hukuk": [False, False]
    # }
    topic_buckets = defaultdict(list)

    # -------------------------------------------------
    # 1) Attempt kayıtlarını konuya göre grupla
    # -------------------------------------------------
    for row in attempt_rows:

        # Attempt kaydından konu bilgisi alınır.
        # Bu alan load_attempts() fonksiyonundan gelmelidir.
        konu = row.get("konu")

        # Attempt kaydından doğru/yanlış bilgisi alınır.
        # True  -> doğru
        # False -> yanlış
        is_correct = row.get("is_correct")

        # Konu bilgisi veya doğru/yanlış bilgisi yoksa
        # bu kayıt analiz dışı bırakılır.
        if konu is None or is_correct is None:
            continue

        # Aynı konuya ait sonuçlar aynı listeye eklenir.
        topic_buckets[konu].append(is_correct)

    # Hesaplanan konu istatistikleri bu listede tutulur.
    stats = []

    # -------------------------------------------------
    # 2) Her konu için metrikleri hesapla
    # -------------------------------------------------
    for konu, results in topic_buckets.items():

        # Bu konudan kaç soru çözülmüş?
        n_questions = len(results)

        # Bu konuda kaç doğru yapılmış?
        #
        # Not:
        # sum(results) sadece True/False verileri için çalışır.
        # Burada daha kontrollü olmak için sadece True olanları sayıyoruz.
        n_correct = sum(1 for r in results if r is True)

        # Yanlış sayısı:
        # toplam soru - doğru soru
        n_wrong = n_questions - n_correct

        # Başarı oranı hesaplanır.
        # n_questions sıfır olamaz ama güvenlik için kontrol bırakılır.
        accuracy = (n_correct / n_questions) * 100 if n_questions > 0 else 0.0

        # Veri yeterlilik durumu belirlenir.
        #
        # Eğer kullanıcı bu konuda min_n kadar veya daha fazla soru çözmüşse
        # analiz daha güvenilir kabul edilir.
        #
        # Aksi halde bu konu "yetersiz" olarak işaretlenir.
        data_status = "yeterli" if n_questions >= min_n else "yetersiz"

        # Hesaplanan istatistik listeye eklenir.
        stats.append(
            {
                "konu": konu,
                "n_questions": n_questions,
                "n_correct": n_correct,
                "n_wrong": n_wrong,
                "accuracy": round(accuracy, 1),
                "data_status": data_status,
            }
        )

    # Konu bazlı istatistikler döndürülür.
    return stats