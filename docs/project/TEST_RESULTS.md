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

## TR-F0-01 - Secret yönetimi ve depo güvenliği doğrulaması

- Run ID: `TR-F0-01`
- Tarih: `2026-07-27`
- Görev: `F0-01`
- Branch: `intent-retrieval-upgrade`
- Git commit: `fb71eb8`
- Durum: `BAŞARILI`

### Doğrulananlar

- Paylaşılmış gizli değerler iptal edilip yenilendi.
- Kod içindeki sabit PostgreSQL kimlik bilgileri kaldırıldı.
- `.env.example` dosyasındaki gerçek görünümlü değerler boş örneklere çevrildi.
- Yerel `.env` dosyasının `.gitignore` tarafından yok sayıldığı doğrulandı.
- Gerçek `.env` dosyasının Git tarafından izlenmediği doğrulandı.
- Git tarafından yalnızca `.env.example` dosyasının izlendiği doğrulandı.
- Aktif Gemini API anahtarının mevcut dosyalarda ve Git geçmişinde bulunmadığı doğrulandı.
- Eksik ortam değişkenlerinde uygulamanın gizli değerleri göstermeden kontrollü hata verdiği doğrulandı.

### Kanıt

- `.gitignore:13:.env`
- `git ls-files .env .env.example` çıktısı: yalnızca `.env.example`
- Güvenlik commit'i: `fb71eb8`
- Commit mesajı: `security: remove hardcoded credentials`

### Sonuç

F0-01 tamamlanma kriterleri karşılandı. Güvenlik görevi belge kapanışına hazırdır.

## TR-F0-02 - Depo ve legacy temizliği teknik doğrulaması

- Run ID: `TR-F0-02`
- Tarih: `2026-08-06`
- Görev: `F0-02`
- Branch: `intent-retrieval-upgrade`
- Git commit: `d3f22fa` (F0-02 çalışma ağacı henüz commit edilmedi)
- Durum: `BAŞARILI`

### Çalıştırılan kontroller

```text
python3 -m compileall -q analysis app backend document_parser evaluation retrieval scripts storage tests
python3 -m tests.intent.run_tests v1
python3 -m tests.intent.run_tests v2
python3 -m tests.intent.run_tests v3
python3 -m tests.intent.run_tests v4
python3 -m tests.intent.run_tests v5
cd frontend && npm run lint
cd frontend && npm run build
git diff --check
```

Ek olarak yasaklı tracked/untracked/ignored dosya desenleri, hassas içerik ve
kaldırılan legacy dosyalara yönelik import, çalışma zamanı, build ve deployment
referansları tarandı.

### Sonuçlar

- Python compile kontrolü başarılıdır.
- Intent runner v1-v5 komutlarının her biri görünür olarak 60/60 ve exit 0
  üretmiştir.
- Frontend lint başarılıdır.
- Frontend production build başarılıdır; yalnızca 500 kB üzeri bundle uyarısı
  verilmiştir.
- `git diff --check` başarılıdır.
- Yasaklı dosya ve hassas içerik taraması başarılıdır; tracked gerçek sır yoktur.
- Kaldırılan 21 dosyaya yönelik aktif kırık referans bulunmamıştır.
- Testlerin oluşturduğu `__pycache__` ve `frontend/dist/` çıktıları ignored'dır;
  yeni tracked veya normal untracked dosya oluşmamıştır.

### Bilinen sınırlamalar

- Mevcut runner v4 için v2, v5 için v3 vakalarını yüklediğinden v4/v5'in görünen
  60/60 sonuçları gerçek set doğrulaması değildir. Sorun `ISSUE-005` içinde
  kayıtlıdır ve F0-02 kapanışını engellemez.
- Aktif `fastapi` ve `pydantic` importlarının `requirements.txt` içinde açık
  karşılığı yoktur. Sorun `ISSUE-003` içinde kayıtlıdır ve F0-02 temizliğinin
  oluşturduğu regression değildir.

### Sonuç

F0-02 zorunlu depo taraması, legacy import kontrolü ve teknik kapanış doğrulamaları
başarılıdır. Bu kayıt F0-03'ün başlatıldığı anlamına gelmez.
