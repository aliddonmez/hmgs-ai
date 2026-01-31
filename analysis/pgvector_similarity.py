# analysis/pgvector_similarity.py
import os
import sys
from typing import List, Tuple, Optional

# Proje root'unu Python path'ine ekle
# Böylece üst klasördeki modülleri (analysis.db gibi) import edebiliyoruz
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from sentence_transformers import SentenceTransformer
from analysis.db import get_conn  # PostgreSQL bağlantısı sağlayan fonksiyon

# 🔹 Global embedding modeli (tek sefer yüklenir)
# Bu model metinleri vektöre çevirir (semantic anlam çıkarır)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# DB’den gelecek satır formatı:
# (başlık, içerik, benzerlik skoru)
Row = Tuple[str, str, float]


def _guess_topic(question: str) -> str:
    """
    Basit topic tahmini (keyword bazlı).
    Amaç: retrieval karışmasını azaltmak.
    Örneğin: Dolandırıcılık sorusunda hırsızlık chunk'ları gelmesin.
    """
    q = question.lower()  # Küçük harfe çevirerek karşılaştırma kolaylaştırılır

    # Her suç tipi için anahtar kelimeler
    fraud_kw = ["dolandır", "hile", "aldat", "aldan", "yarar", "menfaat"]
    theft_kw = ["hırsız", "zilyet", "alma hareketi", "rızanın olmaması", "taşınır"]
    intent_kw = ["kast", "olası kast", "doğrudan kast"]
    negligence_kw = ["taksir", "bilinçli taksir", "özen", "dikkat"]
    tort_kw = ["haksız fiil", "illiyet", "tazminat", "kusur"]
    contract_kw = ["sözleşme", "teklif", "kabul", "irade beyanı"]

    # Soru içinde kelime geçiyorsa ilgili topic döndürülür
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

    # Hiçbiri değilse bilinmeyen konu
    return "unknown"


def _title_matches_topic(title: str, topic: str) -> bool:
    """
    Topic'e göre başlık filtresi.
    Şimdilik sadece başlıkta anahtar kelime arıyoruz.

    ⚠️ İleride DB’ye 'topic' kolonu ekleyip SQL WHERE topic=... yapmak daha doğru olur.
    """
    t = title.lower()

    # Her topic için başlıkta aranacak kelimeler
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

    # Topic bilinmiyorsa filtreleme yapılmaz
    return True


def retrieve(
    question: str,
    top_k: int = 5,          # Sonuç olarak dönecek maksimum chunk sayısı
    fetch_k: int = 20,       # DB’den ilk etapta çekilecek aday sayısı
    min_score: float = 0.60, # Minimum benzerlik skoru eşiği
    use_topic_filter: bool = True,  # Topic filtresi açık mı
    debug: bool = False,     # Debug çıktıları yazdırılsın mı
) -> List[Row]:
    """
    RAG retrieval pipeline:

    1️-Soru embedding'e çevrilir  
    2- pgvector ile en benzer fetch_k aday çekilir  
    3- (Opsiyonel) topic filtresi uygulanır  
    4- min_score altındaki sonuçlar elenir  
     top_k sonuç döndürülür
    """

    conn = get_conn()        # PostgreSQL bağlantısı aç
    cur = conn.cursor()      # Cursor oluştur

    # Soruyu vektöre çevir
    q_emb = model.encode(question).tolist()

    # pgvector ile cosine distance benzeri arama
    # <=> operatörü: vector distance
    # 1 - distance = similarity
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

    # İlk aday sonuçlar
    rows: List[Row] = cur.fetchall()

    cur.close()
    conn.close()

    #  Ham sonuçları görmek için debug modu
    if debug:
        print("\n=== RETRIEVAL DEBUG (RAW candidates) ===")
        print("Q:", question)
        for i, (title, _content, score) in enumerate(rows[:10], start=1):
            print(f"{i:02d}. score={score:.4f} | {title}")
        print("==========================================\n")

    # Topic tahmini
    topic = _guess_topic(question) if use_topic_filter else "no_topic"

    if debug:
        print(f"[DEBUG] topic={topic} | min_score={min_score} | fetch_k={fetch_k} | top_k={top_k}")

    # 1️⃣ Topic filtresi
    if use_topic_filter and topic != "unknown":
        rows = [r for r in rows if _title_matches_topic(r[0], topic)]

    # 2️⃣ Minimum skor filtresi
    rows = [r for r in rows if r[2] >= min_score]

    # 3️⃣ En iyi top_k sonucu al
    rows = rows[:top_k]

    # 🔍 Filtre sonrası debug çıktısı
    if debug:
        print("\n=== RETRIEVAL DEBUG (AFTER topic+min_score) ===")
        print("Q:", question)
        for i, (title, _content, score) in enumerate(rows, start=1):
            print(f"{i:02d}. score={score:.4f} | {title}")
        print("==============================================")

    return rows  # RAG pipeline’a gönderilecek son chunk listesi
