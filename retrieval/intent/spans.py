def extract_reference_spans(query: str, reference_signals: dict) -> dict:
    """
    Sorudaki açık referans parçalarını ayırır.
    """
    return {
        "spans": reference_signals.get("matched_patterns", []),
        "article_numbers": reference_signals.get("detected_article_numbers", []),
        "has_reference": reference_signals.get("has_reference_marker", False),
    }


def extract_relation_spans(
    query: str,
    comparison_signals: dict,
    definition_signals: dict,
    reference_spans: dict,
) -> dict:
    """
    Sorudaki ilişki parçalarını ayırır.
    """
    spans: list[str] = []
    relation_type_hint = None

    if reference_spans.get("has_reference") and "ne diyor" in query:
        spans.append("ne diyor")
        relation_type_hint = "reference_lookup"

    if comparison_signals.get("has_comparison_marker"):
        spans.extend(comparison_signals.get("matched_patterns", []))
        relation_type_hint = "comparison"

    if relation_type_hint is None and definition_signals.get("has_definition_marker"):
        spans.extend(definition_signals.get("matched_patterns", []))
        relation_type_hint = "definition"

    return {
        "spans": list(dict.fromkeys(spans)),
        "relation_type_hint": relation_type_hint,
    }