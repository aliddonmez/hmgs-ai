# analysis/user_report.py

from collections import defaultdict

from app.sqlstorage import load_attempts
from analysis.quizanalysis import compute_topic_stats
from analysis.rank_topics import rank_weak_topics
from analysis.suggestions import generate_study_suggestions


def _compute_group_stats(rows: list, group_key: str) -> list:
    """
    Belirli bir alana göre gruplama yaparak başarı istatistiği üretir.

    Örnek:
    group_key = "subject"    → ders bazlı istatistik
    group_key = "difficulty" → zorluk bazlı istatistik
    """
    buckets = defaultdict(list)

    for r in rows:
        key = r.get(group_key)
        is_correct = r.get("is_correct")

        if key is None or is_correct is None:
            continue

        buckets[key].append(is_correct is True)

    stats = []
    for key, results in buckets.items():
        n = len(results)
        n_correct = sum(results)
        stats.append({
            "label": key,
            "n_questions": n,
            "n_correct": n_correct,
            "n_wrong": n - n_correct,
            "accuracy": round((n_correct / n) * 100, 1) if n > 0 else 0.0,
        })

    return sorted(stats, key=lambda x: x["accuracy"])


def get_user_report(user_id: str, min_n: int = 3) -> dict:
    """
    Belirli bir kullanıcı için performans raporu üretir.

    Dönen yapı:
    {
        "summary": genel başarı özeti,
        "weak_topics": zayıf konular,
        "strong_topics": güçlü konular,
        "insufficient_data_topics": veri yetersiz konular,
        "suggestions": çalışma önerileri,
        "topic_stats": tüm konu istatistikleri,
        "subject_stats": ders bazlı istatistikler,
        "difficulty_stats": zorluk bazlı istatistikler
    }
    """

    rows = load_attempts(user_id)

    if not rows:
        return {
            "summary": {
                "total_questions": 0,
                "accuracy": 0.0,
                "correct": 0,
                "wrong": 0,
            },
            "weak_topics": [],
            "strong_topics": [],
            "insufficient_data_topics": [],
            "suggestions": ["Henüz analiz yapılacak veri yok."],
            "topic_stats": [],
            "subject_stats": [],
            "difficulty_stats": [],
        }

    total   = len(rows)
    correct = sum(1 for r in rows if r.get("is_correct"))
    wrong   = total - correct
    accuracy = round((correct / total) * 100, 1)

    topic_stats = compute_topic_stats(rows, min_n=min_n)
    ranked      = rank_weak_topics(topic_stats)

    # Ders (subject) ve zorluk (difficulty) bazlı istatistikler
    # load_attempts() artık questions JOIN'i ile bu alanları döndürüyor
    subject_stats    = _compute_group_stats(rows, "subject")
    difficulty_stats = _compute_group_stats(rows, "difficulty")

    weak = []
    strong = []
    insufficient = []

    for t in ranked:
        if t["data_status"] == "yetersiz":
            insufficient.append({
                "konu":       t["konu"],
                "n":          t["n_questions"],
                "n_questions": t["n_questions"],
                "min_n":      min_n,
                "message": (
                    f"Bu konuda yeterli veri yok ({t['n_questions']} soru). "
                    f"En az {min_n} soru çözülmeli."
                ),
            })
        elif t["accuracy"] < 60:
            weak.append(t)
        else:
            strong.append(t)

    suggestions = generate_study_suggestions(weak)

    return {
        "summary": {
            "total_questions": total,
            "accuracy": accuracy,
            "correct": correct,
            "wrong": wrong,
        },
        "weak_topics":              weak,
        "strong_topics":            strong,
        "insufficient_data_topics": insufficient,
        "suggestions":              suggestions,
        "topic_stats":              ranked,
        "subject_stats":            subject_stats,
        "difficulty_stats":         difficulty_stats,
    }