import re
from document_parser.text_cleaner import clean_text


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

    # Madde başlangıcını yakalayan kalıp (Örn: "Madde 157-")
    madde_pattern = re.compile(r"^\s*Madde\s+(\d+)\s*[-–—]", re.IGNORECASE)

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = madde_pattern.search(line)

        if match:
            # Yeni bir madde bulduk! Önceki maddeyi paketleyip listeye ekleyelim.
            if current_madde_no:
                # Mevcut içeriğin en son satırı aslında BU YENİ maddenin başlığıdır (TCK formatı).
                # Onu metinden çıkarıp (pop) bir sonraki başlık yapıyoruz.
                if len(current_content) > 0:
                    potential_title = current_content.pop()
                    # Eğer son satır çok uzunsa veya nokta ile bitiyorsa başlık değil, cümledir (Yanlış alarm engelleme)
                    if len(potential_title.split()) > 15 or potential_title.endswith(
                        "."
                    ):
                        current_content.append(potential_title)  # Cümleyse geri koy
                        next_title = "Belirtilmemiş Başlık"
                    else:
                        next_title = potential_title
                else:
                    next_title = "Belirtilmemiş Başlık"

                # Önceki maddeyi kaydet
                results.append(
                    {
                        "doc_id": f"tck_{current_madde_no}",
                        "title": f"TCK Madde {current_madde_no} - {current_title}",  # Başlığı buraya da ekledik
                        "metadata": {
                            "madde_no": current_madde_no,
                            "madde_basligi": current_title,  # VECTOR DB İÇİN ALTIN DEĞERİNDEKİ KISIM
                        },
                        "content": " ".join(current_content),
                    }
                )

                current_title = next_title  # Yeni başlığı sonraki maddeye ata
            else:
                # İlk maddeye (Madde 1) geldiğimizde, üstteki son satır onun başlığıdır.
                if len(current_content) > 0:
                    current_title = current_content[-1]
                    current_content.clear()

            # Yeni maddenin numarasını ve ilk satırını ayarla
            current_madde_no = match.group(1)
            current_content = [line]
        else:
            # Madde başlangıcı değilse metni okumaya devam et
            current_content.append(line)

    # Döngü bitince en son kalan maddeyi de listeye ekle
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
