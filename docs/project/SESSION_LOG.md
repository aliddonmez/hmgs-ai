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

## 2026-07-27 - F0-01 güvenlik görevi kapanışı

### Tamamlanan işlemler

- Paylaşılmış PostgreSQL parolası değiştirildi.
- Kod içindeki sabit PostgreSQL parolaları kaldırıldı.
- Yeni gizli değerler yalnızca yerel `.env` dosyasında tutuldu.
- `.env` dosyasının Git tarafından izlenmediği doğrulandı.
- `.env.example` içindeki gerçek görünümlü gizli değerler kaldırıldı.
- Aktif Gemini API anahtarının mevcut dosyalarda bulunmadığı doğrulandı.
- Aktif Gemini API anahtarının Git geçmişinde bulunmadığı doğrulandı.
- Güvenlik değişiklikleri `fb71eb8` commit'iyle `intent-retrieval-upgrade` branch'ine gönderildi.

### Doğrulama sonucu

- F0-01 tamamlandı.
- `ISSUE-001` çözüm şartları karşılandı.
- Aktif görev `F0-02 - Depo ve legacy dosya temizliği` olarak belirlendi.
- Mevcut kullanıcı değişiklikleri korunarak F0-02'ye devredildi.

### Korunacak mevcut çalışma dosyaları

- `frontend/package-lock.json`
- `retrieval/intent/candidates.py`
- `retrieval/pipeline.py`
- `retrieval/scoring.py`
- `changes.txt`
- `hmgs-ai-clean.zip`

### Sıradaki tek görev

- `F0-02 - Depo ve legacy dosya temizliği`

## SESSION-2026-08-06-01 - F0-02 depo ve legacy temizliği kapanışı

- Tarih/saat: 2026-08-06
- Aktif görev: `F0-02 - Depo ve legacy dosya temizliği`
- Branch: `intent-retrieval-upgrade`
- Başlangıç commit: `d3f22fa`
- Bitiş commit: Oluşturulmadı
- Sorumlu: Ürün sahibi ve teknik inceleme

### Oturum hedefi

Legacy dosya envanterini kanıta dayalı biçimde temizlemek, depo koruma kurallarını
güçlendirmek ve F0-02 kapanış doğrulamalarını tamamlamak.

### Başlangıç durumu

- F0-01 tamamlanmıştı.
- Legacy API, SQLite, Streamlit, deneysel script, eski şema ve scaffold dosyaları
  ayrıntılı salt okunur inceleme bekliyordu.
- Altı kullanıcı değişikliği korunacaktı.

### Yapılan değişiklikler

- 12 gruptaki toplam 21 legacy dosya kaldırıldı.
- Eski Streamlit ve SQLite çalışma zamanı akışları kaldırıldı.
- `requirements.txt` içinden yalnızca kullanılmayan `streamlit` kaldırıldı.
- Kök `.gitignore` ortam varyantı, yerel DB, arşiv/yedek, cache, editör ve geçici
  dosya desenleriyle güçlendirildi.
- `DEC-019` ile legacy temizleme kararı kaydedildi.
- `hmgs-ai-clean.zip` diskte korundu ve ignored yapıldı.
- `changes.txt`, `frontend/package-lock.json`, `retrieval/intent/candidates.py`,
  `retrieval/pipeline.py` ve `retrieval/scoring.py` kullanıcı değişiklikleri
  korunmuştur.

### Değişen dosyalar

- 21 onaylı tracked dosya silmesi.
- `.gitignore`
- `requirements.txt`
- `docs/project/DECISIONS.md`
- F0-02 kapanış takip belgeleri.

### Çalıştırılan testler

| Komut/suite | Sonuç | Run ID |
|---|---|---|
| Python compileall (aktif dizinler) | Başarılı | TR-F0-02 |
| Intent runner v1-v5 | Görünür 60/60; v4/v5 yanlış set | TR-F0-02 |
| Frontend `npm run lint` | Başarılı | TR-F0-02 |
| Frontend `npm run build` | Başarılı; bundle uyarısı | TR-F0-02 |
| Yasaklı dosya ve hassas içerik taraması | Başarılı | TR-F0-02 |
| Legacy import/runtime/build/deployment referans kontrolü | Başarılı | TR-F0-02 |
| `git diff --check` | Başarılı | TR-F0-02 |

### Alınan kararlar

- `DEC-019`: İncelenen 12 gruptaki 21 legacy dosyanın kaldırılması onaylandı.
- F0-02 kapanışı F0-03'ün başlatıldığı anlamına gelmez.

### Yeni sorunlar

- Yeni sorun açılmadı. Runner v4/v5 sınırlaması `ISSUE-005`, eksik açık
  FastAPI/Pydantic bağımlılıkları `ISSUE-003` içinde zaten kayıtlıdır.

### Çözülen sorunlar

- `ISSUE-002`: Depo hijyeni ve yerel artifact riski.
- `ISSUE-029`: Güvensiz legacy `scenario_api.py` yüzeyi.

### Blokerler

- F0-02 kapanışı için bloker yoktur.

### Sıradaki tek görev

- Kullanıcı açıkça onaylarsa `F0-03 - Python bağımlılıklarını standardize et`;
  henüz başlatılmadı.

### Yeni sohbet için devir notu

Önce F0-02 değişikliklerinin commit durumunu ve korunan kullanıcı değişikliklerini
doğrula. Kullanıcı açık izni olmadan F0-03'e geçme.

## SESSION-2026-08-14-01 - F0-03 Python bağımlılık standardizasyonu kapanışı

- Tarih/saat: 2026-08-14
- Aktif görev: `F0-03 - Python bağımlılıklarını standardize et`
- Branch: `intent-retrieval-upgrade`
- Başlangıç commit: `9ac938a`
- Bitiş commit: Bu kaydı içeren F0-03 kapanış commit'i
- Sorumlu: Ürün sahibi ve teknik inceleme

### Oturum hedefi

Python çalışma sürümünü, production/development bağımlılık yapısını ve direct pin
politikasını belirleyip temiz ortamda tekrar üretilebilir backend kurulumunu
doğrulamak.

### Başlangıç durumu

- F0-02 tamamlanmış ve `9ac938a` commit'iyle remote branch'e gönderilmişti.
- `requirements.txt` aktif FastAPI backend'i tam tanımlamıyor ve sürüm pinleri
  içermiyordu.
- Kanonik Python sürümü ile development requirements dosyası yoktu.

### Yapılan değişiklikler

- Python 3.11.x kanonik çalışma serisi ve Python 3.10 syntax alt sınırı belgelendi.
- `.python-version` içine `3.11` eklendi.
- On doğrudan bağımlılık exact pinlendi; transitif paketler doğrudan listelenmedi.
- `requirements-dev.txt`, `-r requirements.txt` içerecek biçimde eklendi.
- README'ye production/development kurulumları ve Uvicorn başlatma hedefi eklendi.
- Pytest F1-02, Alembic F2-02 ve izleme sağlayıcısı paketi F12 kapsamına bırakıldı.

### Değişen dosyalar

- `README.md`
- `requirements.txt`
- `requirements-dev.txt`
- `.python-version`
- F0-03 kapanış takip belgeleri

### Çalıştırılan testler

| Komut/suite | Sonuç | Run ID |
|---|---|---|
| Temiz ortam `pip install -r requirements-dev.txt` | Başarılı | TR-F0-03 |
| `python -m pip check` | Başarılı | TR-F0-03 |
| 10 exact pin ve dependency importu | Başarılı | TR-F0-03 |
| 41 güvenli aktif proje modülü importu | Başarılı | TR-F0-03 |
| `backend.main:app` ve Uvicorn hedefi | Başarılı | TR-F0-03 |
| Python compileall | Başarılı | TR-F0-03 |
| Intent runner v1-v5 | Görünür 60/60; v4/v5 yanlış set | TR-F0-03 |
| `git diff --check` | Başarılı | TR-F0-03 |

### Metrik farkı

Bu çalışma dependency tekrar üretilebilirliğini doğrular; F1-05 kanonik RAG
baseline'ı veya ürün kalite metriği değildir.

### Alınan kararlar

- `DEC-020`: Python 3.11 ve doğrudan bağımlılık pinleme standardı onaylandı.

### Yeni sorunlar

- Yeni sorun açılmadı. Intent runner sınırlaması `ISSUE-005` içinde açık kalır.

### Çözülen sorunlar

- `ISSUE-003`: Python requirements aktif uygulamayı tam tanımlamıyordu.

### Blokerler

- F0-03 kapanışı için bloker yoktur.

### Sıradaki tek görev

- `F0-04 - Frontend bağımlılıklarını standardize et`; başlatılmadı ve kullanıcı
  açık onayı bekleniyor.

### Yeni sohbet için devir notu

F0-03 değişikliklerinin commit durumunu ve korunan kullanıcı değişikliklerini
doğrula. F0-02'nin gerçek kapanış commit'i `9ac938a`'dır. Kullanıcı açık izni
olmadan F0-04'e veya başka göreve geçme.
