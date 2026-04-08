# retrieval/scoring.py

import re

STOPWORDS = {
    "ve", "veya", "ile", "için", "olan", "olarak",
    "bir", "bu", "da", "de", "mi", "mı", "mu", "mü",
    "ne", "nedir", "suçu", "suç", "gibi"
}


def normalize_for_match(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\sçğıöşü]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> list[str]:
    normalized = normalize_for_match(text)
    tokens = normalized.split()

    cleaned_tokens = []
    for token in tokens:
        if len(token) < 2:
            continue
        if token in STOPWORDS:
            continue
        cleaned_tokens.append(token)

    return cleaned_tokens


def lexical_overlap_score(query: str, content: str) -> float:
    query_tokens = set(tokenize(query))
    content_tokens = set(tokenize(content))

    if not query_tokens:
        return 0.0

    overlap = query_tokens.intersection(content_tokens)
    return len(overlap) / len(query_tokens)


def extract_heading_from_content(content: str) -> str:
    content = content.strip()

    if not content:
        return ""

    parts = content.split(" - ")

    # Örnek:
    # "TCK Madde 141 - Hırsızlık - Madde 141- ..."
    # burada ilk 2 parçayı heading gibi alıyoruz
    if len(parts) >= 2:
        return " - ".join(parts[:2])

    return parts[0]


def title_match_score(query: str, title: str) -> float:
    if not title:
        return 0.0

    query_tokens = set(tokenize(query))
    title_tokens = set(tokenize(title))

    if not query_tokens or not title_tokens:
        return 0.0

    overlap = query_tokens.intersection(title_tokens)

    if not overlap:
        return 0.0

    return len(overlap) / len(query_tokens)


def exact_title_match_bonus(query: str, title: str) -> float:
    if not title:
        return 0.0

    query_tokens = set(tokenize(query))
    title_tokens = set(tokenize(title))

    if not query_tokens or not title_tokens:
        return 0.0

    overlap = query_tokens.intersection(title_tokens)

    if not overlap:
        return 0.0

    # TAM EŞLEŞME
    if title_tokens.issubset(query_tokens):
        return 1.0

    overlap_ratio = len(overlap) / len(title_tokens)

    if overlap_ratio >= 0.7:
        return 0.5

    if overlap_ratio >= 0.4:
        return 0.25

    return 0.0

def phrase_match_score(query: str, content: str) -> float:
    query_norm = normalize_for_match(query)
    content_norm = normalize_for_match(content)

    if query_norm in content_norm:
        return 1.0

    return 0.0