from retrieval.query_expansion import expand_query
from retrieval.topic_classifier import classify_topic
from retrieval.vector_search import vector_search
from retrieval.reranker import rerank_chunks


def retrieve_chunks(
    question: str,
    fetch_k: int = 50,
    rerank_k: int = 15,
    top_k: int = 10,
):

    # 1️⃣ Query expansion
    expanded_query = expand_query(question)

    # 2️⃣ Topic classification
    topic = classify_topic(expanded_query)

    # 3️⃣ Vector search
    candidates = vector_search(expanded_query, fetch_k)

    if not candidates:
        return []

    # ------------------------------------------------
    # 4️⃣ SOFT TOPIC BOOST
    # ------------------------------------------------
    boosted = []

    for c in candidates:

        score = float(c["score"])

        if topic and c.get("konu"):
            if topic.lower() in c["konu"].lower():
                score += 0.05

        c["score"] = score
        boosted.append(c)

    boosted = sorted(boosted, key=lambda x: x["score"], reverse=True)

    # ------------------------------------------------
    # 5️⃣ MIN SCORE FILTER
    # ------------------------------------------------
    filtered = [c for c in boosted if c["score"] >= 0.35]

    if not filtered:
        return []

    # ------------------------------------------------
    # 6️⃣ DOC DIVERSITY (MADDE BAZLI)
    # ------------------------------------------------
    per_doc_limit = 2
    per_doc_counts = {}

    diversified = []

    for c in filtered:

        content = c.get("content") or ""

        if "Madde" in content:
            key = content.split("-")[0]  # Madde 21
        else:
            key = c["doc_id"]

        per_doc_counts[key] = per_doc_counts.get(key, 0) + 1

        if per_doc_counts[key] <= per_doc_limit:
            diversified.append(c)

    # ------------------------------------------------
    # 7️⃣ RERANK
    # ------------------------------------------------
    rerank_input = diversified[:rerank_k]

    ranked = rerank_chunks(expanded_query, rerank_input)

    # ------------------------------------------------
    # 8️⃣ TOP K
    # ------------------------------------------------
    return ranked[:top_k]
