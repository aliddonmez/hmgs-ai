import re


def normalize_intent_query(question: str) -> str:
    """
    Intent analizi için soruyu standartlaştırır.
    """
    text = question.lower()
    text = re.sub(r"[^\w\sçğıöşü\.]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text