import re

from retrieval.query_expansion import PHRASE_TERMS, EXPANSION_PACKS
from retrieval.intent.patterns import STOPWORD_TOKENS
from retrieval.intent.spans import (
    extract_reference_spans,
    extract_relation_spans,
)


def _build_phrase_registry() -> list[str]:
    phrases = set(PHRASE_TERMS)

    for pack in EXPANSION_PACKS.values():
        for term, expansions in pack.items():
            if " " in term:
                phrases.add(term)
            for item in expansions:
                if " " in item:
                    phrases.add(item)

    return sorted(phrases, key=len, reverse=True)


PHRASE_REGISTRY = _build_phrase_registry()


def extract_phrase_candidates(
    query: str,
    reference_spans: dict,
    relation_spans: dict,
) -> list[dict]:
    """
    Çok kelimeli kavram adaylarını çıkarır.
    Hem registry hem query içi n-gram üretir.
    """

    # 1️⃣ Maskleme (reference ve relation çıkar)
    masked_query = query

    for ref in reference_spans.get("spans", []):
        masked_query = masked_query.replace(ref, " ")

    for rel in relation_spans.get("spans", []):
        masked_query = masked_query.replace(rel, " ")

    masked_query = re.sub(r"\s+", " ", masked_query).strip()

    tokens = masked_query.split()

    candidates: list[dict] = []

    # -----------------------------------
    # 2️⃣ REGISTRY PHRASE’LER (mevcut)
    # -----------------------------------
    for phrase in PHRASE_REGISTRY:
        if phrase in masked_query:
            candidates.append({
                "text": phrase,
                "normalized_text": phrase,
                "confidence": 0.95,
                "source": "registry_phrase",
            })

    # -----------------------------------
    # 3️⃣ N-GRAM PHRASE ADAYLARI (YENİ)
    # -----------------------------------

    # 2'li ve 3'lü kombinasyonlar
    ngram_candidates = []

    for n in [2, 3, 4]:
        for i in range(len(tokens) - n + 1):
            gram_tokens = tokens[i:i+n]
            gram = " ".join(gram_tokens)

            relation_type_hint = relation_spans.get("relation_type_hint")

            # Comparison sorularında tüm hedef alanını tek n-gram yapma.
            # Örnek: "kast taksir farkı" -> "kast taksir" tek target olmamalı.
            if relation_type_hint == "comparison" and n == len(tokens):
                continue

            # stopword ağırlıklıysa alma
            valid_tokens = [
                t for t in gram_tokens
                if t not in STOPWORD_TOKENS and not t.isdigit()
            ]

            if len(valid_tokens) < n:  # çok zayıf phrase
                continue

            ngram_candidates.append(gram)

    # -----------------------------------
    # 4️⃣ N-GRAM’leri candidate’a ekle
    # -----------------------------------

    for gram in ngram_candidates:
        candidates.append({
            "text": gram,
            "normalized_text": gram,
            "confidence": 0.80,
            "source": "ngram_phrase",
        })

    # -----------------------------------
    # 5️⃣ Tekrar temizliği
    # -----------------------------------

    deduped: list[dict] = []
    seen = set()

    for cand in candidates:
        key = cand["normalized_text"]
        if key not in seen:
            seen.add(key)
            deduped.append(cand)

    return deduped


def extract_token_candidates(
    query: str,
    reference_spans: dict,
    relation_spans: dict,
    phrase_candidates: list[dict],
) -> list[dict]:
    """
    Phrase dışında kalan anlamlı tek kelimeli adayları çıkarır.
    """
    masked_query = query

    for ref in reference_spans.get("spans", []):
        masked_query = masked_query.replace(ref, " ")

    for rel in relation_spans.get("spans", []):
        masked_query = masked_query.replace(rel, " ")

    for phrase in phrase_candidates:
        masked_query = masked_query.replace(phrase["normalized_text"], " ")

    masked_query = re.sub(r"\s+", " ", masked_query).strip()

    candidates: list[dict] = []

    for token in masked_query.split():
        if len(token) < 2:
            continue
        if token in STOPWORD_TOKENS:
            continue
        if token.isdigit():
            continue

        candidates.append({
            "text": token,
            "normalized_text": token,
            "confidence": 0.70,
            "source": "token",
        })

    deduped: list[dict] = []
    seen = set()
    for cand in candidates:
        key = cand["normalized_text"]
        if key not in seen:
            seen.add(key)
            deduped.append(cand)

    return deduped

def appears_outside_longer_target(query: str, short_text: str, longer_texts: list[str]) -> bool:
    """
    Kısa target'ın, uzun target dışında bağımsız olarak geçip geçmediğini kontrol eder.
    """
    short_count = len(re.findall(rf"\b{re.escape(short_text)}\b", query))

    inside_count = 0
    for longer in longer_texts:
        inside_count += len(re.findall(rf"\b{re.escape(short_text)}\b", longer))

    return short_count > inside_count


def merge_target_candidates(
    query: str,
    phrase_candidates: list[dict],
    token_candidates: list[dict],
    reference_spans: dict,
    relation_spans: dict,
) -> list[dict]:
    """
    Phrase ve token adaylarını mantıklı target listesine dönüştürür.

    Kural:
    - reference varsa target dönme
    - comparison ilişkisinde target silme
    - comparison dışı durumlarda, daha uzun target'ın içinde kalan kısa target'ı ele
    """
    if reference_spans.get("has_reference"):
        return []

    merged = list(phrase_candidates) + list(token_candidates)

    # tekrar temizliği
    deduped: list[dict] = []
    seen = set()
    for cand in merged:
        key = cand["normalized_text"]
        if key not in seen:
            seen.add(key)
            deduped.append(cand)

    relation_type_hint = relation_spans.get("relation_type_hint")

    # comparison değilse:
    # daha kısa target, daha uzun bir target'ın içinde geçiyorsa ele
    final_targets: list[dict] = []

    for cand in deduped:
        cand_text = cand["normalized_text"]

        contained_in_longer = False
        for other in deduped:
            other_text = other["normalized_text"]

            if cand_text == other_text:
                continue

            # cand, other'ın gerçek alt parçasıysa ve other daha uzunsa
            if len(other_text) > len(cand_text) and cand_text in other_text:
                longer_texts = [
                    item["normalized_text"]
                    for item in deduped
                    if len(item["normalized_text"]) > len(cand_text)
                    and cand_text in item["normalized_text"]
                ]

                if appears_outside_longer_target(query, cand_text, longer_texts):
                    contained_in_longer = False
                else:
                    contained_in_longer = True

                break

        if not contained_in_longer:
            final_targets.append(cand)

    return final_targets


def extract_intent_targets(query: str, signals: dict) -> list[dict]:
    """
    Nihai target listesini üretir.
    """
    reference_signals = signals.get("reference", {})
    comparison_signals = signals.get("comparison", {})
    definition_signals = signals.get("definition", {})

    reference_spans = extract_reference_spans(query, reference_signals)
    relation_spans = extract_relation_spans(
        query=query,
        comparison_signals=comparison_signals,
        definition_signals=definition_signals,
        reference_spans=reference_spans,
    )
    phrase_candidates = extract_phrase_candidates(
        query=query,
        reference_spans=reference_spans,
        relation_spans=relation_spans,
    )
    token_candidates = extract_token_candidates(
        query=query,
        reference_spans=reference_spans,
        relation_spans=relation_spans,
        phrase_candidates=phrase_candidates,
    )

    merged = merge_target_candidates(
    query=query,
    phrase_candidates=phrase_candidates,
    token_candidates=token_candidates,
    reference_spans=reference_spans,
    relation_spans=relation_spans,
)

    if not merged and not reference_spans.get("has_reference"):
        fallback_query = query
        for rel in relation_spans.get("spans", []):
            fallback_query = fallback_query.replace(rel, " ")
        fallback_query = re.sub(r"\s+", " ", fallback_query).strip()

        if fallback_query:
            merged = [{
                "text": fallback_query,
                "normalized_text": fallback_query,
                "confidence": 0.55,
                "source": "fallback",
            }]

    relation_type_hint = relation_spans.get("relation_type_hint")
    tokens = query.split()

    if relation_type_hint is None and len(merged) == 1:
        if len(tokens) >= 2:
            return [
                {
                    "text": tok,
                    "normalized_text": tok,
                    "confidence": 0.7,
                    "source": "fallback_token"
                }
                for tok in tokens
                if tok not in STOPWORD_TOKENS and not tok.isdigit()
            ]

    return merged

    
    