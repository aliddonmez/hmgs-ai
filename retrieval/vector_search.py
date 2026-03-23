## retrieval/vector_search.py

from analysis.db import get_conn
from retrieval.embedding_model import embed_text


def vector_search(question: str, fetch_k: int = 50):

    conn = get_conn()
    cur = conn.cursor()

    q_emb = embed_text(question).tolist()

    cur.execute(
        """
        SELECT
            d.title,
            dc.content,
            1 - (dc.embedding <=> %s::vector) AS similarity,
            d.id,
            d.ders,
            d.konu
        FROM document_chunks dc
        JOIN documents d ON d.id = dc.document_id
        ORDER BY dc.embedding <=> %s::vector
        LIMIT %s
        """,
        (q_emb, q_emb, fetch_k),
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    results = []

    for title, content, score, doc_id, ders, konu in rows:

        results.append(
            {
                "title": title,
                "content": content,
                "score": score,
                "doc_id": doc_id,
                "ders": ders,
                "konu": konu,
            }
        )
        # 🔎 DEBUG
    print("\n=== VECTOR SEARCH DEBUG ===")
    print("Top results:")
    for r in results[:5]:
        print(
            "DOC:",
            r["doc_id"],
            "| SCORE:",
            round(float(r["score"]), 4),
            "| KONU:",
            r["konu"],
            "| PREVIEW:",
            r["content"][:80],
        )
    print("===========================\n")
    return results
