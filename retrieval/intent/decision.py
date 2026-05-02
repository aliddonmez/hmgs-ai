def build_reference_info(query: str, reference_signals: dict) -> dict:
    return {
        "has_reference": reference_signals.get("has_reference_marker", False),
        "article_numbers": reference_signals.get("detected_article_numbers", []),
        "raw_matches": reference_signals.get("matched_patterns", []),
    }


def infer_relation_type(signals: dict, reference_info: dict, targets: list[dict]) -> str | None:
    if reference_info.get("has_reference"):
        return "reference_lookup"

    comparison_signal = signals.get("comparison", {}).get("has_comparison_marker", False)
    definition_signal = signals.get("definition", {}).get("has_definition_marker", False)

    if comparison_signal and len(targets) >= 2:
        return "comparison"

    if definition_signal:
        return "definition"

    return None


def decide_intent_type(
    relation_type: str | None,
    reference_info: dict,
    targets: list[dict],
) -> dict:
    if reference_info.get("has_reference"):
        return {
            "intent_type": "reference",
            "confidence": 0.95,
            "is_reliable": True,
        }

    target_count = len(targets)

    if relation_type == "comparison" and target_count >= 2:
        return {
            "intent_type": "comparison",
            "confidence": 0.90,
            "is_reliable": True,
        }

    if relation_type == "definition":
        if target_count == 1:
            return {
                "intent_type": "single_focus",
                "confidence": 0.82,
                "is_reliable": True,
            }

        if target_count >= 2:
            return {
                "intent_type": "multi_definition",
                "confidence": 0.80,
                "is_reliable": True,
            }

    return {
        "intent_type": "unknown",
        "confidence": 0.45,
        "is_reliable": False,
    }


def infer_scope_level(
    intent_type: str,
    targets: list[dict],
    reference_info: dict,
) -> str:
    if reference_info.get("has_reference"):
        return "narrow"

    if intent_type == "comparison":
        return "structured_comparison"

    if intent_type == "multi_definition":
        return "broad"

    if len(targets) == 1:
        return "narrow"

    if len(targets) > 1:
        return "broad"

    return "unknown"