# retrieval/topic_classifier.py
from retrieval.embedding_model import embed_text
from sklearn.metrics.pairwise import cosine_similarity

TOPICS = {
    "hırsızlık": "hırsızlık başkasına ait taşınır malın rızası olmadan alınması",
    "dolandırıcılık": "dolandırıcılık suçu hile ile aldatma ve menfaat sağlama",
    "kast": "kast suçun bilerek ve isteyerek işlenmesi",
    "taksir": "taksir dikkat ve özen yükümlülüğüne aykırılık",
}

_topic_embeddings = None


## konuları embedding yapıyoruz en başta sürekli embedding yapmak maliyetli olur cünkü
def _build_topic_embeddings():
    global _topic_embeddings

    if _topic_embeddings is None:
        _topic_embeddings = {topic: embed_text(desc) for topic, desc in TOPICS.items()}

    return _topic_embeddings


def classify_topic(question: str):

    _topic_embeddings = _build_topic_embeddings()

    q_emb = embed_text(question)

    best_topic = None
    best_score = -1

    ## soru ve topic vektörü benzerliği ölçülür .
    for topic, emb in _topic_embeddings.items():
        score = cosine_similarity([q_emb], [emb])[0][0]

        if score > best_score:
            best_score = score
            best_topic = topic

    return best_topic
