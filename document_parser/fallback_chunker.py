from typing import List


def chunk_text(text: str, max_chars: int = 900, overlap: int = 150) -> List[str]:
    """
    Statute parser çalışmazsa genel fallback chunking.
    """
    text = text.strip()

    if not text:
        return []

    chunks = []
    i = 0

    while i < len(text):
        end = min(len(text), i + max_chars)
        chunks.append(text[i:end])

        i = end - overlap
        if i < 0:
            i = 0

        if end == len(text):
            break

    return chunks
