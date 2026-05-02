# Chatbot Aktif Akışı

## Aktif chatbot dosyaları
- `app/ui/chat_page.py` → kullanıcı arayüzü (soru alır, cevap gösterir)
- `app/rag_pipeline.py` → chatbot ana akış ve orkestrasyon
- `retrieval/pipeline.py` → retrieval (veri bulma) akışını yönetir
- `retrieval/query_expansion.py` → sorgu genişletme
- `retrieval/topic_classifier.py` → yardımcı konu tespiti
- `retrieval/vector_search.py` → aday chunk’ları getirir
- `retrieval/reranker.py` → adayları yeniden sıralar
- `app/llm/gemini_client.py` → LLM (Gemini) çağrısı
- `retrieval/config.py` → retrieval ayarları ve debug flag’ler

---

## Resmi chatbot akışı
`chat_page.py -> rag_pipeline.py -> retrieval/pipeline.py -> query_expansion.py -> topic_classifier.py -> vector_search.py -> reranker.py -> rag_pipeline.py -> gemini_client.py -> chat_page.py`

---

## Aktif olmayan (legacy / dikkat edilmesi gereken) dosyalar
Bu dosyalar şu an chatbot akışında aktif olarak kullanılmamaktadır ve yanlışlıkla kullanılırsa kafa karışıklığına sebep olabilir:

- `analysis/pgvector_similarity.py`
- `scripts/seed_db.py`
- `data/day2_texts.py`

---

## Not
Chatbot geliştirmeleri yapılırken sadece yukarıdaki **aktif akış** dikkate alınmalıdır.  
Mimari özellikle değiştirilmediği sürece legacy dosyalar ana geliştirme sürecine dahil edilmemelidir.