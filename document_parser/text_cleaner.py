import re


def clean_text(text: str) -> str:
    """
    Genel metin temizliği:
    - URL satırlarını at
    - sayfa numarası satırlarını at (16/108 gibi)
    - tarih satırlarını at
    - fazla boşlukları normalize et
    """

    lines = text.splitlines()
    cleaned = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # URL içeren satırlar
        if "http://" in line or "https://" in line:
            continue

        # sayfa numarası: 16/108
        if re.match(r"^\d+\s*/\s*\d+$", line):
            continue

        # tarih içeren satırlar: 21.12.2025
        if re.search(r"\d{2}\.\d{2}\.\d{4}", line):
            continue

        # çok kısa / gürültülü satırlar
        if len(line) < 2:
            continue

        cleaned.append(line)

    text = "\n".join(cleaned)

    # boşluk normalize
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n\n", text)

    return text.strip()
