# retrieval/query_expansion.py

import re

# ----------------------------------------
# 1. PHRASE TERMS (İFADELER / KALIPLAR)
# ----------------------------------------
PHRASE_TERMS = [
    "olası kast",
    "bilinçli taksir",
    "taşınır mal",
    "zilyedinin rızası",
]

# ----------------------------------------
# 2. EXPANSION PACKS (GENİŞLETME PAKETLERİ)
# ----------------------------------------
EXPANSION_PACKS = {
    "criminal_law_core": {
        "hırsızlık": [
            "taşınır mal",
            "zilyet",
            "rıza",
            "almak",
        ],
        "dolandırıcılık": [
            "hile",
            "aldatma",
            "menfaat",
        ],
        "taksir": [
            "dikkat",
            "özen",
            "kusur",
            "bilinçli taksir",
        ],
        "kast": [
            "doğrudan kast",
            "olası kast",
            "bilerek",
            "isteyerek",
        ],
        "taşınır mal": [
            "zilyet",
            "rıza",
            "başkasına ait",
        ],
    }
}

# ----------------------------------------
# 3. NORMALIZE (STANDARTLAŞTIRMA)
# ----------------------------------------
def normalize_query(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\sçğıöşü]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ----------------------------------------
# 4. PHRASE HITS (İFADE EŞLEŞMELERİ)
# ----------------------------------------
def find_phrase_hits(query: str) -> list[str]:
    phrase_hits = []

    for phrase in PHRASE_TERMS:
        if phrase in query:
            phrase_hits.append(phrase)

    return phrase_hits

# ----------------------------------------
# 5. MATCHED TERMS (EŞLEŞEN TERİMLERİ BUL)
# ----------------------------------------
def find_matched_terms(query: str) -> list[str]:
    matched_terms = []

    for pack in EXPANSION_PACKS.values():
        for term in pack.keys():
            if term in query:
                matched_terms.append(term)

    return matched_terms

# ----------------------------------------
# 6. EXPANSION (GENİŞLETME)
# ----------------------------------------
def build_expanded_query(query: str, matched_terms: list[str]) -> tuple[str, list[str]]:
    added_terms = []

    for pack in EXPANSION_PACKS.values():
        for term in matched_terms:
            if term in pack:
                for candidate_term in pack[term]:
                    # sorguda zaten varsa tekrar ekleme
                    if candidate_term in query:
                        continue
                    added_terms.append(candidate_term)

    # tekrarları temizle ama sırayı koru
    added_terms = list(dict.fromkeys(added_terms))

    if added_terms:
        expanded_query = query + " " + " ".join(added_terms)
    else:
        expanded_query = query

    return expanded_query.strip(), added_terms

# ----------------------------------------
# 7. ANA FONKSİYON
# ----------------------------------------
def expand_query(question: str) -> dict:
    normalized_query = normalize_query(question)

    phrase_hits = find_phrase_hits(normalized_query)
    matched_terms = find_matched_terms(normalized_query)

    # phrase'leri de matched_terms içine dahil et
    all_matched_terms = list(dict.fromkeys(matched_terms + phrase_hits))

    expanded_query, added_terms = build_expanded_query(
        normalized_query,
        all_matched_terms
    )

    return {
        "original_query": question,
        "normalized_query": normalized_query,
        "phrase_hits": phrase_hits,
        "matched_terms": all_matched_terms,
        "added_terms": added_terms,
        "expanded_query": expanded_query,
    }