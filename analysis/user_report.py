# analysis/user_report.py
from app.sqlstorage import load_attempts
from analysis.quizanalysis import compute_topic_stats
from analysis.rank_topics import rank_weak_topics
from analysis.suggestions import generate_study_suggestions


def get_user_report(user_id: str, min_n: int = 3) -> dict:
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
        }

    total = len(rows)
    correct = sum(1 for r in rows if r.get("is_correct"))
    wrong = total - correct
    accuracy = round((correct / total) * 100, 1)

    topic_stats = compute_topic_stats(rows, min_n=min_n)
    ranked = rank_weak_topics(topic_stats)

    weak, strong, insufficient = [], [], []

    for t in ranked:
        if t["data_status"] == "yetersiz":
            insufficient.append(
                {
                    "konu": t["konu"],
                    "n": t["n_questions"],
                    "min_n": min_n,
                    "message": (
                        f"Bu konuda yeterli veri yok ({t['n_questions']} soru). "
                        f"En az {min_n} soru çözülmeli."
                    ),
                }
            )
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
        "weak_topics": weak,
        "strong_topics": strong,
        "insufficient_data_topics": insufficient,
        "suggestions": suggestions,
        "topic_stats": ranked,
    }
