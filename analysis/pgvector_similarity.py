# analysis/pgvector_similarity.py
import os
import sys
from typing import List, Tuple, Optional

# ✅ Proje root'unu Python path'ine ekle
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from sentence_transformers import SentenceTransformer
from analysis.db import get_conn

# 🔹 Global embedding modeli (tek sefer yüklenir)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

Row = Tuple[str, str, float]  # (title, content, similarity)


def _guess_topic(question: str) -> str:
    """
    Basit topic tahmini (keyword).
    Amaç: retrieval karışmasını azaltmak (fraud sorusuna theft chunk gelmesin gibi).
    """
    q = question.lower()

    fraud_kw = ["dolandır", "hile", "aldat", "aldan", "yarar", "menfaat"]
    theft_kw = ["hırsız", "zilyet", "alma hareketi", "rızanın olmaması", "taşınır"]
    intent_kw = ["kast", "olası kast", "doğrudan kast"]
    negligence_kw = ["taksir", "bilinçli taksir", "özen", "dikkat"]
    tort_kw = ["haksız fiil", "illiyet", "tazminat", "kusur"]
    contract_kw = ["sözleşme", "teklif", "kabul", "irade beyanı"]

    if any(k in q for k in fraud_kw):
        return "fraud"
    if any(k in q for k in theft_kw):
        return "theft"
    if any(k in q for k in intent_kw):
        return "intent"
    if any(k in q for k in negligence_kw):
        return "negligence"
    if any(k in q for k in tort_kw):
        return "tort"
    if any(k in q for k in contract_kw):
        return "contract"
    return "unknown"


def _title_matches_topic(title: str, topic: str) -> bool:
    """
    Topic -> allowed title keyword mapping (minimum viable).
    Daha sonra DB'ye 'topic' kolonu ekleyip SQL WHERE topic=... ile daha temiz olur.
    """
    t = title.lower()

    if topic == "fraud":
        return ("dolandır" in t) or ("hile" in t)
    if topic == "theft":
        return ("hırsız" in t) or ("zilyet" in t) or ("alma" in t)
    if topic == "intent":
        return "kast" in t
    if topic == "negligence":
        return "taksir" in t
    if topic == "tort":
        return "haksız fiil" in t
    if topic == "contract":
        return "sözleşme" in t or "teklif" in t or "kabul" in t
    # unknown -> filtresiz
    return True


def retrieve(
    question: str,
    top_k: int = 5,
    fetch_k: int = 20,
    min_score: float = 0.60,
    use_topic_filter: bool = True,
    debug: bool = False,
) -> List[Row]:
    """
    RAG retrieval:
    - soruyu embed eder
    - pgvector ile fetch_k aday çeker
    - (opsiyonel) topic filtresi uygular
    - min_score altını eler
    - top_k döndürür
    """
    conn = get_conn()
    cur = conn.cursor()

    q_emb = model.encode(question).tolist()

    cur.execute(
        """
        SELECT
            title,
            content,
            1 - (embedding <=> %s::vector) AS similarity
        FROM hukuki_kaynaklar
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        """,
        (q_emb, q_emb, fetch_k),
    )
    rows: List[Row] = cur.fetchall()

    cur.close()
    conn.close()

    if debug:
        print("\n=== RETRIEVAL DEBUG (RAW candidates) ===")
        print("Q:", question)
        for i, (title, _content, score) in enumerate(rows[:10], start=1):
            print(f"{i:02d}. score={score:.4f} | {title}")
        print("==========================================\n")

    topic = _guess_topic(question) if use_topic_filter else "no_topic"

    if debug:
        print(f"[DEBUG] topic={topic} | min_score={min_score} | fetch_k={fetch_k} | top_k={top_k}")

    # 1) Topic filtresi
    if use_topic_filter and topic != "unknown":
        rows = [r for r in rows if _title_matches_topic(r[0], topic)]

    # 2) Min score filtresi
    rows = [r for r in rows if r[2] >= min_score]

    # 3) Top-k
    rows = rows[:top_k]

    if debug:
        print("\n=== RETRIEVAL DEBUG (AFTER topic+min_score) ===")
        print("Q:", question)
        for i, (title, _content, score) in enumerate(rows, start=1):
            print(f"{i:02d}. score={score:.4f} | {title}")
        print("==============================================")

    return rows