import re

from retrieval.intent.patterns import (
    COMPARISON_PATTERNS,
    DEFINITION_PATTERNS,
    REFERENCE_PATTERNS,
)


def detect_reference_signals(query: str) -> dict:
    matched_patterns: list[str] = []
    detected_article_numbers: list[str] = []

    for pattern in REFERENCE_PATTERNS:
        matches = re.findall(pattern, query)
        if matches:
            matched_patterns.extend(matches)

    if matched_patterns:
        detected_article_numbers = re.findall(r"\b\d+\b", query)

    return {
        "has_reference_marker": len(matched_patterns) > 0,
        "matched_patterns": list(dict.fromkeys(matched_patterns)),
        "detected_article_numbers": list(dict.fromkeys(detected_article_numbers)),
    }


def detect_comparison_signals(query: str) -> dict:
    matched_patterns: list[str] = []

    for pattern in COMPARISON_PATTERNS:
        if pattern in query:
            matched_patterns.append(pattern)

    return {
        "has_comparison_marker": len(matched_patterns) > 0,
        "matched_patterns": list(dict.fromkeys(matched_patterns)),
    }


def detect_definition_signals(query: str) -> dict:
    matched_patterns: list[str] = []

    for pattern in DEFINITION_PATTERNS:
        if pattern in query:
            matched_patterns.append(pattern)

    return {
        "has_definition_marker": len(matched_patterns) > 0,
        "matched_patterns": list(dict.fromkeys(matched_patterns)),
    }