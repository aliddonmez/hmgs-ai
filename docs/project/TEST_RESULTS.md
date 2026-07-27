# HMGS Chatbot - Test Sonuçları

## Belge amacı

Bu belge önemli test/evaluation koşularının insan tarafından okunabilir özetini tutar.
Sonuçlar ortam, model, veri ve commit bilgisi olmadan kanonik kabul edilmez.

## Sonuç durumları

- `GOZLEM`: Kod incelemesi veya eski çıktıdan elde edilen, yeniden üretilecek sonuç.
- `BASELINE`: Kontrollü ortamda F1-05 kapsamında yeniden üretilmiş başlangıç sonucu.
- `ADAY`: Yeni değişiklik sonucu; kalite kapısı henüz onaylanmadı.
- `ONAYLI`: İlgili kalite kapısından geçmiş sonuç.

# TR-000 - İlk proje incelemesi gözlemleri

- Durum: `GOZLEM`
- Tarih: 2026-07-14
- Kaynak: Kullanıcının paylaştığı `hmgs-ai 3.zip`
- Git commit: Arşiv temiz çıkarımında kullanılamadı
- DB: Paylaşılan PostgreSQL dump/çalışma ortamı; kanonik sürüm belirsiz
- Embedding modeli: Ortam dosyası ve örnek dosyada farklı adlar görüldü
- Reranker: `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`
- LLM: Kodda `gemini-2.5-flash`

Bu sonuçlar ürün baseline'ı değildir. F0 ve F1 tamamlandıktan sonra temiz ve sürümlü
ortamda yeniden çalıştırılacaktır.

## TR-000-A - Python sözdizimi/import ön kontrolü

Çalıştırılan kontrol:

```text
python3 -m compileall
```

Sonuç:

- İncelenen aktif Python dizinleri sözdizimi derlemesini geçti.
- Bu kontrol runtime bağımlılığı, DB veya işlevsel doğruluk kanıtı değildir.

## TR-000-B - Intent test çalıştırıcı gözlemi

Mevcut `tests/intent/run_tests.py` ile görünen sonuç:

| Parametre | Görünen sonuç | Gerçekte yüklenen set |
|---|---:|---|
| v1 | 60/60 | v1 |
| v2 | 60/60 | v2 |
| v3 | 60/60 | v3 |
| v4 | 60/60 | Yanlışlıkla v2 |
| v5 | 60/60 | Yanlışlıkla v3 |

Test runner atlanıp gerçek test dosyaları doğrudan çalıştırıldığında:

| Gerçek set | Sonuç |
|---|---:|
| v1 | 60/60 |
| v2 | 60/60 |
| v3 | 60/60 |
| v4 | 60/60 |
| v5 | 45/60 |
| Toplam | 285/300 (%95) |

Bilinen v5 başarısızlık grubu:

- `kast taksir nedir`,
- `suç kusur nedir`,
- `fail mağdur nedir`,
- `ceza yaptırım nedir`,
- Benzer çoklu tanım sorguları.

Sistem bu soruların bir bölümünü `multi_definition` yerine `single_focus` ve iki hedef
yerine tek hedef olarak sınıflandırmaktadır.

Karar:

- F1-01 tamamlanmadan 300/300 sonucu geçerli kabul edilmeyecek.
- F1-05 sırasında gerçek baseline yeniden kaydedilecek.

## TR-000-C - Mevcut kayıtlı retrieval evaluation

Kaynak:

```text
evaluation/eval_output.txt
```

Sonuç:

| Grup | Doğru | Toplam | Oran |
|---|---:|---:|---:|
| Single article | 22 | 27 | %81,48 |
| Comparison | 0 | 5 | %0 |
| Concept | 0 | 6 | %0 |
| Other | 0 | 2 | %0 |
| Genel | 22 | 40 | %55 |

Yorum:

- Bu evaluation ürün hedefini doğru ölçmemektedir.
- Comparison soruları birden fazla gerekli madde yerine `uncertain` olarak tanımlıdır.
- Concept/other vakalarında answer/no-answer beklentisi retrieval doğruluğuyla
  karıştırılmıştır.
- Sonuç, retrieval'ın zayıf olduğuna işaret eder ancak kanonik ürün metriği değildir.

Bilinen örnek başarısızlık:

```text
Soru: taksirle öldürme nedir
Beklenen: TCK 85
Gelen: TCK 22
```

Query expansion genel taksir kavramlarını ekleyerek TCK 22'yi gereğinden fazla
güçlendirmiştir.

## TR-000-D - Frontend temiz kurulum

Çalıştırılan kontrol:

```text
npm ci
```

Sonuç: Başarısız.

Neden:

- `package.json` ile `package-lock.json` senkron değildir.
- Eksik peer bağımlılık kayıtları raporlanmıştır.

Etkisi:

- Yeni bir ortamda deterministik frontend kurulumu yapılamamaktadır.

Hedef görev: F0-04.

## TR-000-E - Proje paketleme ve güvenlik gözlemi

Arşivde görülenler:

- Gerçek `.env`,
- Gerçek görünümlü Gemini anahtarı,
- Veritabanı şifresi,
- `.venv`,
- `node_modules`,
- `.git`,
- İç içe ZIP,
- Cache ve işletim sistemi artıkları.

Bu bir otomatik secret scan sonucu değildir; inceleme gözlemidir. F0-01'de anahtar
rotasyonu ve kanonik secret scan sonucu ayrıca kaydedilecektir.

# Kanonik baseline şablonu

F1-05 tamamlandığında aşağıdaki bölüm doldurulacaktır:

```text
Run ID:
Durum: BASELINE
Tarih:
Git commit:
Branch:
Python/Node sürümü:
DB migration sürümü:
TCK kaynak sürümü/hash:
Parser/chunking sürümü:
Embedding model/index sürümü:
Reranker sürümü:
Prompt sürümü:
LLM modeli:

Intent:
- Genel accuracy:
- Target exact match:
- Article extraction:

Retrieval:
- Recall@1:
- Recall@3:
- Recall@5:
- MRR:
- Soru türü bazında sonuç:

Answer/no-answer:
- False answer:
- False refusal:

Generation:
- Faithfulness:
- Citation accuracy:
- Kaynak dışı madde:

Performans:
- P50:
- P95:
- Hata oranı:
- Tahmini soru maliyeti:

Başarısız vaka ID'leri:
```

# Sonuç ekleme kuralı

Yeni sonuç eklendiğinde:

1. Benzersiz Run ID kullanılır.
2. Eski sonuç değiştirilmez; yeni kayıt eklenir.
3. Ortam ve sürüm alanları boş bırakılamaz.
4. Başarısız vaka ID'leri saklanır.
5. Baseline ile fark açıkça yazılır.
6. İyileşen toplam metrik yanında kötüleşen alt gruplar da raporlanır.
7. Yayın kapısını geçen sonuç `DECISIONS.md` kararına bağlanır.

