from retrieval.query_expansion import expand_query
from retrieval.topic_classifier import classify_topic
from retrieval.vector_search import vector_search
from retrieval.reranker import rerank_chunks
from retrieval.scoring import lexical_overlap_score, title_match_score, exact_title_match_bonus,phrase_match_score
from retrieval.config import DEBUG_META
from retrieval.config import (
    FETCH_K,
    RERANK_K,
    TOP_K,
    MIN_SCORE,
    PER_DOC_LIMIT,
    TOPIC_BOOST,
)


def retrieve_chunks(
    question: str,
    fetch_k: int = FETCH_K,
    rerank_k: int = RERANK_K,
    top_k: int = TOP_K,
):
    # 1️⃣ Query expansion
    expansion_result = expand_query(question)
    expanded_query = expansion_result["expanded_query"]

    print("\n=== QUERY EXPANSION DEBUG ===")
    print("original:", expansion_result["original_query"])
    print("normalized:", expansion_result["normalized_query"])
    print("phrase_hits:", expansion_result["phrase_hits"])
    print("matched_terms:", expansion_result["matched_terms"])
    print("added_terms:", expansion_result["added_terms"])
    print("expanded_query:", expansion_result["expanded_query"])

    # 2️⃣ Topic classification
    topic_result = classify_topic(expanded_query)

    print("\n=== TOPIC CLASSIFIER DEBUG ===")
    print("topic:", topic_result["topic"])
    print("confidence:", topic_result["confidence"])
    print("is_reliable:", topic_result["is_reliable"])

    topic = topic_result["topic"]
    is_reliable = topic_result["is_reliable"]

    # 3️⃣ Vector search
    candidates = vector_search(expanded_query, fetch_k)

    if not candidates:
        return []

    # ------------------------------------------------
    # 4️⃣ SCORING
    # ------------------------------------------------
    scored_candidates = []

    for c in candidates:
        if DEBUG_META:
            meta = c.get("meta", {})
            print(
                f"META DEBUG → madde: {meta.get('madde_no')} | title: {meta.get('title')}"
            )
        content = c.get("content", "")

        vector_score = float(c["score"])
        topic_score = 0.0
        lexical_score = lexical_overlap_score(expanded_query, content)

        meta = c.get("meta", {})
        title = meta.get("title")
        title_score = title_match_score(expanded_query, title)
        phrase_score = phrase_match_score(expanded_query, content)
        exact_title = exact_title_match_bonus(expanded_query, title)

        if is_reliable and topic != "unknown" and c.get("konu"):
            if topic.lower() in c["konu"].lower():
                topic_score = TOPIC_BOOST

        final_score = (
            vector_score
            + topic_score
            + (lexical_score * 0.10)
            + (title_score * 0.20)
            + (exact_title * 0.25)
            + (phrase_score * 0.15 ) 
        )

        c["vector_score"] = vector_score
        c["topic_score"] = topic_score
        c["lexical_score"] = lexical_score
        c["title_score"] = title_score
        c["exact_title"] = exact_title
        c["final_score"] = final_score

        scored_candidates.append(c)

    scored_candidates = sorted(
        scored_candidates,
        key=lambda x: x["final_score"],
        reverse=True
    )

    print("\n=== SCORING DEBUG ===")
    for c in scored_candidates[:5]:
        preview = (c.get("content") or "")[:80].replace("\n", " ")
        print(
            f"VECTOR={c['vector_score']:.4f} | "
            f"TOPIC={c['topic_score']:.4f} | "
            f"LEXICAL={c['lexical_score']:.4f} | "
            f"TITLE={c['title_score']:.4f} | "
            f"EXACT_TITLE={c.get('exact_title', 0.0):.4f} | "
            f"FINAL={c['final_score']:.4f} | "
            f"PREVIEW={preview}"
        )

    # ------------------------------------------------
    # 5️⃣ MIN SCORE FILTER
    # ------------------------------------------------
    filtered = [c for c in scored_candidates if c["final_score"] >= MIN_SCORE]

    if not filtered:
        return []

    # ------------------------------------------------
    # 6️⃣ DOC DIVERSITY (MADDE BAZLI)
    # ------------------------------------------------
    per_doc_counts = {}
    diversified = []

    for c in filtered:
        meta = c.get("meta", {})

        madde_no = meta.get("madde_no")

        if madde_no:
            key = f"{c['doc_id']}_madde_{madde_no}"
        else:
            key = c["doc_id"]

        per_doc_counts[key] = per_doc_counts.get(key, 0) + 1

        if per_doc_counts[key] <= PER_DOC_LIMIT:
            diversified.append(c)

    # ------------------------------------------------
    # 7️⃣ RERANK
    # ------------------------------------------------
    rerank_input = diversified[:rerank_k]
    ranked = rerank_chunks(expanded_query, rerank_input)

    # ------------------------------------------------
    # 8️⃣ RERANK GUARDRAIL
    # ------------------------------------------------

    guarded = []

    for c in ranked:
        vector_score = c.get("vector_score", 0)
        rerank_score = c.get("score", 0)  # reranker skoru burada oluyor

        # ❗ düşük semantic + yüksek rerank varsa ele
        if vector_score < 0.40 and rerank_score > 0.80:
            continue

        guarded.append(c)

    # ------------------------------------------------
    # 8️⃣ TOP K
    # ------------------------------------------------
    return guarded[:top_k]