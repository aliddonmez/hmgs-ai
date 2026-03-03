# analysis/quizanalysis.py

from collections import defaultdict
from typing import List, Dict


def compute_topic_stats(attempt_rows: List[Dict], min_n: int = 3) -> List[Dict]:
    """
    Konu bazlı ham istatistik üretir.
    Girdi: SADECE tek bir kullanıcıya ait attempt_rows
    """

    topic_buckets = defaultdict(list)

    # 1) Konuya göre gruplama yapılıyor analiz icinde konu ve doğru mu yanlış mı oldugunun bilinmesi gerekiyor.
    for row in attempt_rows:
        konu = row.get("konu")
        is_correct = row.get("is_correct")

        if konu is None or is_correct is None:
            continue

        topic_buckets[konu].append(is_correct)

    stats = []

    # 2) Metrikleri üret
    for konu, results in topic_buckets.items():
        n_questions = len(results)  ## bu konuyla karşılaşma sayısı
        n_correct = sum(results)  ## doğru sayısı
        n_wrong = n_questions - n_correct

        accuracy = (
            (n_correct / n_questions) * 100 if n_questions > 0 else 0.0
        )  ##oranlama

        data_status = (
            "yeterli" if n_questions >= min_n else "yetersiz"
        )  ## o konuda belirli sayıda soru çözmediyse yetersiz diye cıktı verioyr .

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

    return stats
