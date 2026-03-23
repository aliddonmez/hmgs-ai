import os


def load_document_text(path: str) -> str:
    """
    txt / pdf / docx dosyalarını düz metne çevirir.
    """
    ext = os.path.splitext(path)[1].lower()

    if ext == ".txt":
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    if ext == ".pdf":
        import fitz

        doc = fitz.open(path)
        parts = []

        for page in doc:
            parts.append(page.get_text("text"))

        return "\n".join(parts)

    if ext == ".docx":
        import docx

        d = docx.Document(path)
        return "\n".join(p.text for p in d.paragraphs)

    raise ValueError(f"Unsupported file type: {ext}")
