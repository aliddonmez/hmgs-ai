# Hallucination Types (HMGS) — Day 6.1 Notları

Bu belge, testlerde görülen hata / risk tiplerini sınıflandırır.

## 1) Dataset-dışı soru (Context yok) — "Doğru susma"
Belirli suçlar veya kavramlar BAĞLAM’da yoksa model cevap vermemeli.
Örnek:
- "Kasten öldürme suçu nedir?"
- "Yağma suçu nedir?"
- "Filtre kahvede ideal kahve–su oranı nedir?"

Beklenen:
- "Bu soruya, elimdeki kaynaklara dayanarak güvenilir bir cevap veremiyorum."

## 2) Retrieval hatası → yanlış reddetme (False Negative)
BAĞLAM’da ilgili metin yokmuş gibi davranıp "BAĞLAM’da yok" demek.
Örnek:
- "Dolandırıcılık suçunda 'hile' ile 'aldatma' aynı şey midir?"
(Bu soruda dolandırıcılık metni BAĞLAM'a gelmediği için model cevap veremedi.)

Risk:
- Kullanıcı sistemde bilgi yok zanneder.

## 3) BAĞLAM var ama model çıkarım yapıyor (Overreach / Yorum)
Model BAĞLAM’da geçmeyen bir sonucu mantıken çıkarıp "kesin" gibi yazarsa risk oluşur.
Örnek:
- Dolandırıcılıkta "iradenin sakatlanması" ifadesinden "rıza geçersizdir" sonucuna gitmek
(Bağlamda rıza etkisi açıkça yazmıyorsa bu HMGS v1 kural ihlaline yaklaşır.)

## 4) Rol/amaç uyumsuz soruya cevap verme (Product mismatch)
BAĞLAM’da bilgi olsa bile sistemin amacı ceza hukuku asistanıysa hukuk dışı sorularda çerçeve koyması gerekir.
Örnek:
- "Ofsayt kuralı nedir?" (BAĞLAM’da var ama hukuk rolüyle çelişiyor)

## 5) Prompt/task mismatch
Soru bir şey sorarken görev başka bir şey istiyorsa (örn. “Kast nedir?” ama görev “hırsızlık tanımı+unsurlar”),
model doğru soruyu değil görev metnini takip edebilir.

Çözüm:
- Prompt şablonunda görev kısmını sabit tutma; soruya göre seç.
- Ya da backend’de “task” alanını dinamik üret.