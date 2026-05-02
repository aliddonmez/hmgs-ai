from retrieval.intent.normalize import normalize_intent_query
from retrieval.intent.signals import (
    detect_reference_signals,
    detect_comparison_signals,
    detect_definition_signals,
)
from retrieval.intent.spans import (
    extract_reference_spans,
    extract_relation_spans,
)
from retrieval.intent.candidates import (
    extract_phrase_candidates,
    extract_token_candidates,
    merge_target_candidates,
    extract_intent_targets,
)

__all__ = [
    "normalize_intent_query",
    "detect_reference_signals",
    "detect_comparison_signals",
    "detect_definition_signals",
    "extract_reference_spans",
    "extract_relation_spans",
    "extract_phrase_candidates",
    "extract_token_candidates",
    "merge_target_candidates",
    "extract_intent_targets",
]