from typing import Any

from retrieval.intent import (
    normalize_intent_query,
    detect_reference_signals,
    detect_comparison_signals,
    detect_definition_signals,
    extract_intent_targets,
)

from retrieval.intent.decision import (
    build_reference_info,
    infer_relation_type,
    decide_intent_type,
    infer_scope_level,
)


def classify_intent(question: str) -> dict[str, Any]:
    normalized_query = normalize_intent_query(question)

    reference_signals = detect_reference_signals(normalized_query)
    comparison_signals = detect_comparison_signals(normalized_query)
    definition_signals = detect_definition_signals(normalized_query)

    signals = {
        "reference": reference_signals,
        "comparison": comparison_signals,
        "definition": definition_signals,
    }

    targets = extract_intent_targets(normalized_query, signals)
    reference_info = build_reference_info(normalized_query, reference_signals)
    relation_type = infer_relation_type(signals, reference_info, targets)
    decision = decide_intent_type(
        relation_type=relation_type,
        reference_info=reference_info,
        targets=targets,
    )

    scope_level = infer_scope_level(
        intent_type=decision["intent_type"],
        targets=targets,
        reference_info=reference_info,
    )

    return {
        "original_query": question,
        "normalized_query": normalized_query,
        "intent_type": decision["intent_type"],
        "confidence": decision["confidence"],
        "is_reliable": decision["is_reliable"],
        "target_count": len(targets),
        "targets": targets,
        "relation_type": relation_type,
        "scope_level": scope_level,
        "reference_info": reference_info,
        "signals": signals,
    }