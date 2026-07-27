# HMGS Chatbot - Çalışma Oturumu Günlüğü

## Belge amacı

Bu dosya sohbetler ve çalışma günleri arasında kısa teknik devir kaydıdır. Ayrıntılı
plan `MASTER_PLAN.md`, güncel tek durum `CURRENT_STATUS.md`, kalıcı kararlar
`DECISIONS.md` içindedir. Bu günlük kronolojik geçmişi korur.

## Yeni kayıt şablonu

```markdown
## SESSION-YYYY-MM-DD-NN - Kısa başlık

- Tarih/saat:
- Aktif görev:
- Branch:
- Başlangıç commit:
- Bitiş commit:
- Sorumlu:

### Oturum hedefi

### Başlangıç durumu

### Yapılan değişiklikler

### Değişen dosyalar

### Çalıştırılan testler

| Komut/suite | Sonuç | Run ID |
|---|---|---|

### Metrik farkı

### Alınan kararlar

### Yeni sorunlar

### Çözülen sorunlar

### Blokerler

### Sıradaki tek görev

### Yeni sohbet için devir notu
```

Kurallar:

- Yeni kayıt dosyanın üstüne değil, kronolojik olarak sonuna eklenir.
- Eski kayıt sessizce değiştirilmez; hata varsa düzeltme notu eklenir.
- Test komutu çalıştırılmadıysa `çalıştırılmadı` açıkça yazılır.
- Commit oluşturulmadıysa commit uydurulmaz.
- Sıradaki tek görev bir `MASTER_PLAN.md` görev kodu taşımalıdır.

# Oturum kayıtları

## SESSION-2026-07-14-01 - Projenin ayrıntılı teknik incelemesi

- Tarih: 2026-07-14
- Aktif görev: Planlama öncesi proje incelemesi
- Branch: Doğrulanamadı; arşiv temiz çıkarımı Git metadata olmadan incelendi
- Başlangıç commit: Bilinmiyor
- Bitiş commit: Oluşturulmadı
- Sorumlu: Teknik inceleme

### Oturum hedefi

Paylaşılan projenin dosya, RAG, intent, retrieval, backend, frontend, veri ve test
yapısını inceleyip ürünleştirme risklerini belirlemek.

### Başlangıç durumu

- 420 MB civarında proje ZIP'i.
- `.venv`, `node_modules`, `.git`, `.env`, DB ve iç içe ZIP içeriyordu.
- Mevcut chatbot TCK + pgvector + MiniLM + cross-encoder + Gemini kullanıyordu.

### Yapılan incelemeler

- 117 kaynak/veri dosyası temiz çıkarımda envanterlendi.
- Python compile ön kontrolü yapıldı.
- Intent test runner ve gerçek v4/v5 dosyaları karşılaştırıldı.
- Kayıtlı retrieval evaluation grupları ayrıştırıldı.
- RAG, scoring, reranker, prompt, DB, API ve frontend okundu.
- Frontend temiz kurulum denendi.

### Çalıştırılan testler

| Kontrol | Sonuç | Run ID |
|---|---|---|
| Python compileall | Başarılı | TR-000-A |
| Intent mevcut runner v1-v5 | Görünür 60/60; v4/v5 yanlış set | TR-000-B |
| Gerçek v4 | 60/60 | TR-000-B |
| Gerçek v5 | 45/60 | TR-000-B |
| Kayıtlı retrieval çıktı analizi | 22/40, %55 | TR-000-C |
| `npm ci` | Başarısız | TR-000-D |

### Temel bulgular

- Reranker guardrail yanlış skor alanını okuyor.
- Reranker sırası RAG katmanında yeniden bozuluyor.
- Intent test runner v4/v5 yanlış import kullanıyor.
- Query expansion bileşik suç sorgusunu bozabiliyor.
- Embedding model adı tutarsız.
- DB şemaları çakışıyor.
- LLM hata metni answer sayılabilir.
- Citation validation yok.
- Gerçek anahtar paylaşılmış.

### Yeni sorunlar

- `KNOWN_ISSUES.md` içinde ISSUE-001 ile ISSUE-030 arasında kaydedildi.

### Sıradaki görev

- Önce kalıcı proje takip belgelerini oluşturmak.

## SESSION-2026-07-14-02 - Ürün kararları ve ana plan

- Tarih: 2026-07-14
- Aktif görev: Ürün kapsamı ve ürünleştirme planı
- Branch: Doğrulanmadı
- Bitiş commit: Oluşturulmadı
- Sorumlu: Ürün sahibi ve teknik planlama

### Onaylanan ürün kararları

- Hedef kullanıcı HMGS öğrencisi.
- İlk kapsam yalnızca güncel TCK.
- Eğitim asistanı; hukuki danışmanlık değil.
- Reference, kavram, karşılaştırma, anlatım, senaryo ve takip soruları.
- Kısa/detaylı/otomatik cevap.
- Konuşma içi hafıza.
- Resmî güncelleme kontrolü + manuel yayın onayı.
- 20-100 kullanıcıyla kapalı beta.
- E-posta hesabı.
- Temel admin paneli ve yapılandırılmış feedback.
- Beta retrieval >= %90, açık yayın >= %95.
- Çoğu cevap 5-8 saniye hedefi.
- İki geliştirici; Ali chatbot çekirdeğinden sorumlu.
- 1-2 ay beta hazırlık hedefi.

### Oluşturulan belgeler

- `PRODUCT_SCOPE.md`
- `MASTER_PLAN.md`
- `ARCHITECTURE.md`

### Doğrulamalar

- Master plan: 16 faz, 72 benzersiz görev.
- Her görevde durum, sorumlu ve tamamlanma kriteri bulunduğu kontrol edildi.
- Mimari belgede mevcut ve hedef sistem ayrıldı.

### Sıradaki görev

- Test, sonuç ve sorun takip belgelerini oluşturmak.

## SESSION-2026-07-14-03 - Test ve devir takip sisteminin tamamlanması

- Tarih: 2026-07-14
- Aktif görev: Proje takip belgeleri
- Branch: Doğrulanmadı
- Bitiş commit: Oluşturulmadı
- Sorumlu: Teknik planlama

### Yapılan değişiklikler

- `TEST_STRATEGY.md` oluşturuldu.
- `TEST_RESULTS.md` oluşturuldu.
- `KNOWN_ISSUES.md` oluşturuldu.
- `CURRENT_STATUS.md` oluşturuldu.
- `DECISIONS.md` oluşturuldu.
- `SESSION_LOG.md` oluşturuldu.

### Doğrulamalar

- Test stratejisi yapı kontrolü yapıldı.
- 30 issue ID'sinin benzersiz olduğu doğrulandı.
- Gözlem sonuçları baseline'dan açıkça ayrıldı.
- 18 onaylı ve 4 açık karar kaydedildi.

### Uygulama kodu durumu

- Uygulama kodunda değişiklik yapılmadı.
- Ürün hataları henüz düzeltilmedi.

### Blokerler

- F0-01 için Gemini anahtarının kullanıcı tarafından sağlayıcı hesabında iptal edilip
  yenilenmesi gerekir.
- Gerçek Git deposu/branch/commit yeni çalışma başlangıcında doğrulanmalıdır.

### Sıradaki tek görev

- `F0-01 - Açığa çıkan anahtarları iptal et ve yenile`.

### Yeni sohbet için devir notu

Takip belgelerini sırayla oku; kod değişikliğine geçmeden önce aktif Git deposunu ve
secret rotasyonunun tamamlanıp tamamlanmadığını doğrula. F0-01 tamamlanmadan eski
Gemini anahtarını kullanma veya hiçbir çıktıda gösterme.
