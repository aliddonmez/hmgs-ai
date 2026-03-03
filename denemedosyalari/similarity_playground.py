# analysis/similarity_playground
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data.day2_texts import TEXTS

from sentence_transformers import SentenceTransformer  ## metni vektöre cevirir 
 
import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))) ## iki vektör aynı yöne mi bakıyor ,  uzunluk değil açı önemli , '1' e yaklaşıldıkca benzerlik artar .

def main():
    # 1) Model
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2") ##model

    # 2) Soru
    question = "Hırsızlık suçu nedir?"
    q_emb = model.encode(question)   ## soru da vektöre cevrilir cünkü vektör vektörle karşılaştırılır . 

    # 3) Metin embedding'leri
    embeddings = []
    for item in TEXTS:
        emb = model.encode(item["text"])
        embeddings.append((item, emb))

    # 4) Similarity hesapla
    scores = []
    for item, emb in embeddings:
        score = cosine_similarity(q_emb, emb)
        scores.append((item["id"], score, item["title"], item["expected_group"])) ##yakınlık uzaklık ölçer  expected_group bizim basta belirttigimiz yakınlık derecesi 

    # 5) Sırala ve yazdır
    scores.sort(key=lambda x: x[1], reverse=True)

    print("QUESTION:", question)
    print("-" * 70)
    for doc_id, score, title, group in scores:
        print(f"Metin {doc_id:>2} -> {score:.4f} | {title} | group={group}")

if __name__ == "__main__":
    main()
