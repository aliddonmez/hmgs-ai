# HMGS Chatbot - Güncel Durum

## Son güncelleme

- Tarih: 2026-08-14
- Proje aşaması: Ürünleştirme hazırlığı
- Aktif faz: `FAZ 0 - Güvenli ve tekrar üretilebilir proje tabanı`
- Aktif görev: `F0-03 - Python bağımlılıklarını standardize et (TAMAMLANDI)`
- Son tamamlanan çalışma: `F0-03 - Python bağımlılıklarını standardize et`
- Sıradaki plan görevi: `F0-04 - Frontend bağımlılıklarını standardize et`
  (başlatılmadı; kullanıcı onayı bekleniyor)
- Çalışma branch'i: `intent-retrieval-upgrade`
- Kanonik önceki Git commit'i: `9ac938a` (F0-02 kapanış commit'i)
- F0-03 kapanış commit'i: Bu kaydı içeren F0-03 commit'i
- Bloker: Yok

## 1. Ürün hedefi

İlk yayın, yalnızca güncel Türk Ceza Kanunu'nu kullanan ve HMGS öğrencilerine yönelik
web tabanlı eğitim chatbotudur. Kişisel hukuki danışmanlık yapmaz. İlk yayın modeli
20-100 kullanıcıyla kapalı betadır.

Ayrıntı: `PRODUCT_SCOPE.md`

## 2. Tamamlanan takip belgeleri

| Belge | Durum | Görev |
|---|---|---|
| `PRODUCT_SCOPE.md` | Tamamlandı | Ürün sınırları ve kalite hedefleri |
| `MASTER_PLAN.md` | Tamamlandı | 16 faz, 72 görev ve kalite kapıları |
| `ARCHITECTURE.md` | Tamamlandı | Mevcut/hedef mimari ve geçiş stratejisi |
| `TEST_STRATEGY.md` | Tamamlandı | Test katmanları, metrikler ve yayın kapıları |
| `TEST_RESULTS.md` | Tamamlandı | İlk inceleme gözlemleri ve baseline şablonu |
| `KNOWN_ISSUES.md` | Tamamlandı | 30 öncelikli sorun |
| `DECISIONS.md` | Tamamlandı | Onaylanmış ürün ve süreç kararları |
| `SESSION_LOG.md` | Tamamlandı | Sohbetler arası devir kaydı ve şablon |

## 3. Son tamamlanan çalışma ve açık uygulama işleri

F0-03, 2026-08-14 tarihinde tamamlandı:

- Python 3.11.x kanonik çalışma serisi, Python 3.10 kaynak kodu sözdizimi alt
  sınırı olarak belgelendi.
- On doğrudan production/runtime bağımlılığı exact pinlendi; transitif paketler
  doğrudan listelenmedi.
- Production ve development kurulumu `requirements.txt` ile
  `requirements-dev.txt` olarak ayrıldı.
- Temiz Python 3.11.5 ortamında development kurulumu, `pip check`, exact pin ve
  dependency import kontrolleri başarılı oldu.
- 41 güvenli aktif proje modülü import edildi; `backend.main:app` FastAPI örneği
  olarak ve README Uvicorn hedefi olarak doğrulandı.
- Compileall ve intent runner v1-v5 komutları exit 0 üretti. ISSUE-005 nedeniyle
  v4/v5'in görünen 60/60 sonuçları gerçek set doğrulaması değildir.
- Gerçek PostgreSQL veya Gemini API bağlantısı kurulmadı.

F0-02, `9ac938a` commit'iyle tamamlandı ve remote branch'e gönderildi.

F0-02, 2026-08-06 tarihinde tamamlandı:

- 12 gruptaki 21 legacy dosya kaldırıldı.
- Aktif import, çalışma zamanı, build veya deployment bağımlılığı kalmadı.
- Eski Streamlit ve SQLite çalışma zamanı akışları kaldırıldı.
- `requirements.txt` içinden yalnızca kullanılmayan `streamlit` kaldırıldı.
- `.gitignore` yerel DB, arşiv/yedek, ortam varyantı, cache ve geçici dosya
  desenleriyle güçlendirildi.
- `hmgs-ai-clean.zip` silinmeden diskte korundu ve ignored yapıldı.
- `changes.txt` ile dört modified kullanıcı dosyası korundu.
- Yasaklı dosya/hassas içerik taraması ve teknik doğrulamalar başarılı oldu.

Henüz yapılmayanlar:

- Frontend bağımlılıkları düzeltilmedi.
- CI kurulmadı.
- Intent test runner v4/v5 hatası düzeltilmedi.
- Pytest dönüşümü yapılmadı.
- Kanonik baseline henüz oluşturulmadı.
- Retrieval/reranker kodu henüz değiştirilmedi.
- Veritabanı migration'ı başlatılmadı.
- Auth, admin paneli veya deployment geliştirilmedi.

Takip belgelerinin oluşturulması ürün kodunun tamamlandığı anlamına gelmez.

## 4. Mevcut doğrulanmış/gözlenen teknik durum

| Alan | Mevcut gözlem | Durum türü |
|---|---:|---|
| Intent v1 | 60/60 | Gözlem |
| Intent v2 | 60/60 | Gözlem |
| Intent v3 | 60/60 | Gözlem |
| Intent v4 gerçek | 60/60 | Gözlem |
| Intent v5 gerçek | 45/60 | Gözlem |
| Intent toplam gerçek | 285/300 (%95) | Gözlem |
| Kayıtlı retrieval | 22/40 (%55) | Eski/hatalı şemalı evaluation |
| Frontend `npm ci` | Başarısız | Doğrudan kontrol |
| Python compile | Başarılı | Sözdizimi ön kontrolü |

Bu değerler F1-05 tamamlanana kadar kanonik baseline değildir.

## 5. En yüksek öncelikli açık sorunlar

1. `ISSUE-005`: Intent v4/v5 yanlış test importu - P1.
2. `ISSUE-007`: Retrieval evaluation yanlış modeli - P1.
3. `ISSUE-012`: Reranker guardrail yanlış skor alanı - P1.
4. `ISSUE-013`: Reranker sırası sonradan bozuluyor - P1.
5. `ISSUE-018`: Gemini hata metni başarılı cevap sayılabilir - P1.
6. `ISSUE-019`: Citation validation yok - P1.
7. `ISSUE-020`: Embedding modeli tutarsız - P1.
8. `ISSUE-021`: Çakışan DB şemaları - P1.
9. `ISSUE-024`: Authentication/veri izolasyonu yok - P1.

Ayrıntı: `KNOWN_ISSUES.md`

## 6. Sıradaki yürütme sırası

```text
F0-01  TAMAMLANDI - Secret rotasyonu
F0-02  TAMAMLANDI - Depo ve legacy temizliği
F0-03  TAMAMLANDI - Python temiz kurulum
F0-04  Sıradaki hedef - Frontend temiz kurulum (başlatılmadı)
F0-05  CI
F1-01  Intent runner v4/v5 düzeltmesi
F1-02  Pytest dönüşümü
F1-03  Retrieval evaluation şeması
F1-04  Metrik motoru
F1-05  Kanonik baseline
```

## 7. Sonraki oturumun ilk kontrol listesi

Yeni sohbet/oturum başladığında:

1. `CURRENT_STATUS.md` okunur.
2. `PRODUCT_SCOPE.md` kapsamı doğrulanır.
3. `MASTER_PLAN.md` içinden aktif görev açılır.
4. `DECISIONS.md` içindeki aktif kararlar kontrol edilir.
5. `KNOWN_ISSUES.md` içindeki ilgili sorunlar bulunur.
6. Son `SESSION_LOG.md` kaydı okunur.
7. Git branch, commit ve çalışma ağacı doğrulanır.
8. Görev öncesi testler çalıştırılır.
9. Kullanıcıya mevcut durum ve yapılacak tek görev özetlenir.
10. Onay/harici işlem gerekmiyorsa uygulamaya geçilir.

## 8. Yeni sohbet başlangıç mesajı

Kullanıcı yeni bir sohbette aşağıdaki mesajı kullanabilir:

> HMGS chatbot projesine kaldığımız yerden devam edeceğiz. Önce
> `docs/project/CURRENT_STATUS.md`, `PRODUCT_SCOPE.md`, `MASTER_PLAN.md`,
> `DECISIONS.md`, `ARCHITECTURE.md`, `TEST_STRATEGY.md`, `TEST_RESULTS.md`,
> `KNOWN_ISSUES.md` ve `SESSION_LOG.md` dosyalarını oku. Aktif görevi, son test
> sonuçlarını, açık riskleri ve sıradaki tek adımı özetle. Kod değiştirmeden önce
> mevcut testleri çalıştır.

## 9. Oturum kapatma kuralı

Her çalışma oturumu kapatılmadan önce:

- Tamamlanan görevler,
- Değişen dosyalar,
- Test komutları ve sonuçları,
- Başarısız testler,
- Alınan kararlar,
- Yeni veya çözülen sorunlar,
- Aktif branch/commit,
- Sıradaki tek görev,
- Blokerler

`SESSION_LOG.md` ve bu dosyaya yazılır.

## 10. Bu dosyayı güncelleme kuralı

Bu dosya yalnızca güncel durumu gösterir. Eski durumlar `SESSION_LOG.md` ve Git
geçmişinde tutulur. Aktif görev değiştiğinde, bir kalite kapısı geçildiğinde veya yeni
bloker oluştuğunda aynı çalışma kapsamında güncellenmelidir.
