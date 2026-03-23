## retrieval / reranker.py

from sentence_transformers import CrossEncoder

_reranker = None


def get_reranker():
    global _reranker

    if _reranker is None:
        _reranker = CrossEncoder("cross-encoder/mmarco-mMiniLMv2-L12-H384-v1")
    return _reranker


def rerank_chunks(question, chunks):
    reranker = get_reranker()

    pairs = [(question, c["content"]) for c in chunks]

    scores = reranker.predict(pairs)
    ## indeksleme
    for i, s in enumerate(scores):
        chunks[i]["rerank_score"] = float(s)

    chunks = sorted(
        chunks,
        key=lambda x: x["rerank_score"],
        reverse=True,
    )

    return chunks
