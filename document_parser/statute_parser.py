import re
from document_parser.text_cleaner import clean_text


NOISE_LINES = {
    "Mevzuat Bilgi Sistemi",
}


def is_valid_title_candidate(line: str) -> bool:
    line = line.strip()

    if not line:
        return False

    if line in NOISE_LINES:
        return False

    # Çok uzunsa büyük ihtimal başlık değildir
    if len(line.split()) > 12:
        return False

    # Cümle gibi bitiyorsa başlık değildir
    if line.endswith(".") or line.endswith(";") or line.endswith(":"):
        return False

    # "Madde ..." satırı başlık değildir
    if re.match(r"^\s*Madde\s+\d+", line, re.IGNORECASE):
        return False

    return True


def find_previous_title(lines: list[str]) -> str:
    """
    Sondan geriye doğru gidip ilk uygun başlığı bulur.
    """
    for line in reversed(lines):
        line = line.strip()
        if is_valid_title_candidate(line):
            return line
    return "Belirtilmemiş Başlık"


def parse_statute_articles(text: str):
    """
    Kanun metnini Madde bazında parçalar ve başlıkları otomatik yakalar.
    """
    text = clean_text(text)
    lines = text.splitlines()

    results = []
    current_madde_no = None
    current_title = "Genel Hükümler"
    current_content = []

    # Madde başlangıcını yakalayan kalıp
    madde_pattern = re.compile(r"^\s*Madde\s+(\d+)\s*[-–—]", re.IGNORECASE)

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = madde_pattern.search(line)

        if match:
            # Yeni maddeye geldik, önce önceki maddeyi kaydet
            if current_madde_no:
                next_title = find_previous_title(current_content)

                # Kaydetmeden önce current_content içinden başlığı temizle
                cleaned_content = current_content[:]
                if cleaned_content and cleaned_content[-1].strip() == next_title:
                    cleaned_content.pop()

                results.append(
                    {
                        "doc_id": f"tck_{current_madde_no}",
                        "title": f"TCK Madde {current_madde_no} - {current_title}",
                        "metadata": {
                            "madde_no": current_madde_no,
                            "madde_basligi": current_title,
                        },
                        "content": " ".join(cleaned_content),
                    }
                )

                current_title = next_title
            else:
                # İlk madde için üstten başlık bul
                if len(current_content) > 0:
                    current_title = find_previous_title(current_content)
                    current_content.clear()

            current_madde_no = match.group(1)
            current_content = [line]
        else:
            current_content.append(line)

    # Son maddeyi de ekle
    if current_madde_no:
        results.append(
            {
                "doc_id": f"tck_{current_madde_no}",
                "title": f"TCK Madde {current_madde_no} - {current_title}",
                "metadata": {
                    "madde_no": current_madde_no,
                    "madde_basligi": current_title,
                },
                "content": " ".join(current_content),
            }
        )

    return results