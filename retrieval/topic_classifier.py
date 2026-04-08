# retrieval/topic_classifier.py

TOPIC_KEYWORDS = {
    "hırsızlık": ["hırsızlık", "zilyet", "taşınır mal"],
    "dolandırıcılık": ["dolandırıcılık", "hile", "aldatma"],
    "taksir": ["taksir", "dikkat", "özen"],
    "kast": ["kast", "olası kast", "bilinçli taksir"],
}


def classify_topic(query: str) -> dict:
    scores = {}

    # basit skor: kaç keyword geçti
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in query:
                score += 1
        scores[topic] = score

    # en iyi ve ikinci en iyi
    sorted_topics = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    best_topic, best_score = sorted_topics[0]
    second_score = sorted_topics[1][1] if len(sorted_topics) > 1 else 0

    # normalize (basit)
    total = sum(scores.values()) + 1e-6
    confidence = best_score / total

    # config değerlerini al
    from retrieval.config import (
        TOPIC_CONFIDENCE_THRESHOLD,
        TOPIC_MARGIN_THRESHOLD,
    )

    margin = best_score - second_score

    # güven kontrolü
    if confidence < TOPIC_CONFIDENCE_THRESHOLD or margin < TOPIC_MARGIN_THRESHOLD:
     f   return {
            "topic": "unknown",
            "confidence": confidence,
            "is_reliable": False,
        }

    return {
        "topic": best_topic,
        "confidence": confidence,
        "is_reliable": True,
    }