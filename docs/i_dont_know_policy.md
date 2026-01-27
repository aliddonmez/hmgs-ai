# “Bilmiyorum / Cevap Vermeme” Politikası (HMGS) — Day 6.1

Amaç:
- Halüsinasyonu (kaynak dışı cevap) engellemek
- Retrieval karışıklığında yanlış güven üretmemek

## Ne zaman cevap vermemeliyiz?

### 1) İlgili ceza hukuku BAĞLAM'ı yoksa
- Soru ceza hukuku kavramı soruyor ama gelen BAĞLAM’da o kavram geçmiyor.

### 2) Gelen BAĞLAM alakasızsa (topic mismatch)
- Örn. futbol/borçlar hukuku metni geliyor ama soru dolandırıcılık/hırsızlık soruyor.

### 3) Retrieval çok zayıfsa (confidence düşük)
- En iyi similarity skoru < X
- veya getirilen ilgili chunk sayısı < K
(Not: X ve K değeri 6.3’te test ile belirlenecek.)

### 4) Modelin cevap vermesi için çıkarım yapması gerekiyorsa
- BAĞLAM açıkça söylemiyor; model ancak yorumla tamamlayabiliyor.
HMGS v1’de bu durumda susmak tercih edilir.

## Cevap vermeme çıktısı (sabit metin)

"Bu soruya, elimdeki kaynaklara dayanarak güvenilir bir cevap veremiyorum."

İsteğe bağlı (debug modunda):
- "İlgili bağlam bulunamadı / düşük güven skoru."