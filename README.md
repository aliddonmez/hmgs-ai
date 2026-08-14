# HMGS AI

HMGS'ye hazırlanan hukuk öğrencileri için
RAG tabanlı yapay zeka destekli öğrenme platformu.

## Python ortamı

Proje için önerilen ve kanonik çalışma serisi Python 3.11.x'tir. Kaynak kodun
sözdizimi alt sınırı Python 3.10'dur; proje doğrulamaları Python 3.11.5 ile
yapılmıştır.

Production/runtime bağımlılıklarını kurmak için:

```bash
python -m pip install -r requirements.txt
```

Development ortamını kurmak için:

```bash
python -m pip install -r requirements-dev.txt
```

`requirements-dev.txt` şu anda production bağımlılıklarını içerir.
Development-only paketler, kendi görevleri uygulandığında eklenecektir.

FastAPI uygulamasını geliştirme modunda başlatmak için:

```bash
python -m uvicorn backend.main:app --reload
```
