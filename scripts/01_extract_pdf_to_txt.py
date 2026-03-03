from pathlib import Path
from pypdf import PdfReader


def pdf_to_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages_text = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages_text.append(text)
        else:
            pages_text.append("")
            print(f"[WARN] Sayfa {i+1} boş: {pdf_path.name}")

    return "\n".join(pages_text)


def main():
    raw_dir = Path("data/raw")
    out_dir = Path("data/raw_txt")
    out_dir.mkdir(parents=True, exist_ok=True)

    for pdf_path in raw_dir.rglob("*.pdf"):
        print(f"[INFO] Okunuyor: {pdf_path}")
        text = pdf_to_text(pdf_path)

        out_file = out_dir / f"{pdf_path.stem}.txt"
        out_file.write_text(text, encoding="utf-8")

        print(f"[OK] Yazıldı: {out_file}\n")


if __name__ == "__main__":
    main()
