## retrieval/embedding_model.py

from sentence_transformers import SentenceTransformer

_model = None


def get_embedding_model():
    global _model

    if _model is None:
        import os
        model_name = os.getenv("EMBED_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        _model = SentenceTransformer(model_name)

    return _model


def embed_text(text: str):
    model = get_embedding_model()
    return model.encode(text)
