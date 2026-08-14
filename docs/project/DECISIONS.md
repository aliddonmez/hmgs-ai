# HMGS Chatbot - Karar Kayıtları

## Belge amacı

Bu belge ürün kapsamını, mimariyi, güvenlik yaklaşımını veya çalışma sırasını etkileyen
kararları ve gerekçelerini saklar. Eski karar silinmez; yeni karar eskisini geçersiz
kılıyorsa iki kayıt birbirine bağlanır.

## Karar durumları

- `ONERILDI`: Henüz onaylanmadı.
- `ONAYLANDI`: Uygulanacak karar.
- `GECERSIZ_KILINDI`: Daha yeni karar tarafından değiştirildi.
- `REDDEDILDI`: Değerlendirildi fakat uygulanmadı.

## Karar şablonu

```text
## DEC-XXX - Başlık
Tarih:
Durum:
Karar veren:
Bağlam:
Karar:
Gerekçe:
Sonuçlar:
Alternatifler:
İlgili görev/sorun:
Yerine geçen/geçersiz kılan karar:
```

# Onaylanmış kararlar

## DEC-001 - İlk ürün yalnızca HMGS öğrencilerine yöneliktir

- Tarih: 2026-07-14
- Durum: `ONAYLANDI`
- Karar veren: Ürün sahibi
- Bağlam: Hedef kullanıcı ürün kapsamını ve cevap biçimini belirler.
- Karar: İlk ürünün birincil kullanıcısı HMGS sınavına hazırlanan öğrencidir.
- Gerekçe: Dar ve ölçülebilir kullanıcı ihtiyacında güvenilir ürün geliştirmek.
- Sonuç: Vatandaş/profesyonel hukuk danışmanlığı kullanım senaryosu desteklenmez.
- İlgili belge: `PRODUCT_SCOPE.md`

## DEC-002 - İlk bilgi kapsamı yalnızca güncel TCK'dır

- Tarih: 2026-07-14
- Durum: `ONAYLANDI`
- Karar veren: Ürün sahibi
- Bağlam: İlk sürüm veri kaynağının sınırlandırılması.
- Karar: Yalnızca güncel ve doğrulanmış Türk Ceza Kanunu kullanılacaktır.
- Gerekçe: Kaynak çeşitliliğinden önce yüksek doğruluk, izlenebilirlik ve güncellik.
- Sonuç: Ders notu, doktrin, yargı kararı ve TCK dışı mevzuat ilk sürümde kullanılmaz.
- Alternatif: Bütün HMGS dersleri veya çoklu kaynak; ilk sürüm için reddedildi.
- İlgili görev: F3, F5, F7.

## DEC-003 - Ürün eğitim asistanıdır, hukuki danışman değildir

- Tarih: 2026-07-14
- Durum: `ONAYLANDI`
- Karar veren: Ürün sahibi
- Karar: Chatbot yalnızca eğitim ve sınava hazırlık amacıyla cevap verecektir.
- Gerekçe: Ürün amacı, güvenlik ve hukuki sorumluluk sınırı.
- Sonuç: Kişisel uyuşmazlıkta kesin sonuç/eylem talimatı verilmez; gerekli durumda
  kapsam sınırı açıklanır.
- İlgili görev: F4-01, F6-04, F7.

## DEC-004 - Desteklenen soru türleri ayrı stratejiler kullanacaktır

- Tarih: 2026-07-14
- Durum: `ONAYLANDI`
- Karar veren: Ürün sahibi ve teknik inceleme
- Karar: Reference, kavram, karşılaştırma, konu anlatımı, kısa eğitim senaryosu ve
  takip soruları desteklenir; tek retrieval/prompt yoluna zorlanmaz.
- Gerekçe: Soru türlerinin kaynak ihtiyacı ve cevap yapısı farklıdır.
- Sonuç: Intent-aware retrieval router ve intent'e özel prompt/evaluation gerekir.
- İlgili görev: F4, F5, F7, F8.

## DEC-005 - Cevap biçimi kısa, detaylı ve otomatik olabilir

- Tarih: 2026-07-14
- Durum: `ONAYLANDI`
- Karar veren: Ürün sahibi
- Karar: Kullanıcı kısa/detaylı seçebilir; seçim yoksa intent'e göre otomatik biçim.
- Sonuç: Biçim değişikliği hukuki kaynak veya sonucu değiştiremez.
- İlgili görev: F7-05.

## DEC-006 - İlk sürüm konuşma içi hafıza kullanır

- Tarih: 2026-07-14
- Durum: `ONAYLANDI`
- Karar veren: Ürün sahibi
- Karar: Aynı sohbet içindeki takip soruları desteklenir; kalıcı sohbet geçmişi ilk
  sürümün zorunlu özelliği değildir.
- Gerekçe: Gerçek chatbot deneyimi sağlarken veri kapsamını sınırlamak.
- Sonuç: Yapılandırılmış, boyutu ve süresi sınırlı conversation state gerekir.
- İlgili görev: F8.

## DEC-007 - Mevzuat değişikliği otomatik yayınlanmayacaktır

- Tarih: 2026-07-14
- Durum: `ONAYLANDI`
- Karar veren: Ürün sahibi
- Karar: Resmî kaynak değişikliği otomatik algılanır; yönetici onayı olmadan aktif
  indekse alınmaz.
- Gerekçe: Bozuk parser, yanlış kaynak veya doğrulanmamış güncellemenin yayına çıkmasını
  engellemek.
- Sonuç: Aday sürüm, diff, onay, indeksleme, smoke test ve rollback gerekir.
- İlgili görev: F3-04, F10-03.

## DEC-008 - İlk yayın kapalı beta olacaktır

- Tarih: 2026-07-14
- Durum: `ONAYLANDI`
- Karar veren: Ürün sahibi
- Karar: İlk yayın 20-100 HMGS öğrencisiyle kapalı beta; kalite kapısı olmadan geniş
  yayın yapılmaz.
- Gerekçe: Gerçek kullanım hatalarını kontrollü ortamda ölçmek.
- Sonuç: Auth, feedback, izleme, destek ve beta GO/no-go kararı gerekir.
- İlgili görev: F14, F15.

## DEC-009 - İlk sürüm basit e-posta hesabı kullanacaktır

- Tarih: 2026-07-14
- Durum: `ONAYLANDI`
- Karar veren: Ürün sahibi
- Karar: Beta kullanıcıları e-posta/parola hesabıyla giriş yapar.
- Gerekçe: Kullanım limiti, veri izolasyonu ve geri bildirim ilişkilendirmesi.
- Sonuç: Güvenli parola hash'i, doğrulama, sıfırlama ve token yönetimi gerekir.
- İlgili görev: F9-02, F9-03.

## DEC-010 - Temel yönetici paneli beta kapsamındadır

- Tarih: 2026-07-14
- Durum: `ONAYLANDI`
- Karar veren: Ürün sahibi
- Karar: TCK sürümü, update adayı, ingest, sistem sağlığı, feedback, kalite ve maliyet
  görünümü bulunan temel panel yapılacaktır.
- Gerekçe: Ürünün DB/script üzerinden kör biçimde yönetilmemesi.
- İlgili görev: F10-03, F10-04.

## DEC-011 - Kullanıcı feedback'i otomatik öğrenme sağlamaz

- Tarih: 2026-07-14
- Durum: `ONAYLANDI`
- Karar veren: Ürün sahibi ve teknik inceleme
- Karar: Feedback önce manuel/yetkili incelemeden geçer; doğrulanırsa regression
  vakasına dönüşür.
- Gerekçe: Yanlış veya kötü niyetli geri bildirimin sistemi bozmasını engellemek.
- Sonuç: İnceleme durumları ve audit izi gerekir.
- İlgili görev: F10-01, F10-02.

## DEC-012 - Beta kalite ve açık yayın eşikleri farklıdır

- Tarih: 2026-07-14
- Durum: `ONAYLANDI`
- Karar veren: Ürün sahibi
- Karar: Kapalı beta için genel retrieval en az %90; açık yayın için en az %95.
- Ek eşikler: Intent >= %95, atıf >= %98, faithfulness >= %95 ve kaynak dışı madde %0.
- Gerekçe: Beta öğrenme ortamıdır; geniş yayın daha yüksek güven gerektirir.
- Sonuç: Tek accuracy yerine soru türü ve risk bazlı kalite kapıları uygulanır.
- İlgili görev: F14-04, F15-04.

## DEC-013 - Konuşmalar yalnızca onayla ve sınırlı süre saklanabilir

- Tarih: 2026-07-14
- Durum: `ONAYLANDI`
- Karar veren: Ürün sahibi
- Karar: Kalite geliştirme için açık bilgilendirme/onay, kişisel veri maskeleme ve
  silme hakkı zorunludur.
- Sonuç: Kesin saklama süresi ayrıca kararlaştırılacaktır.
- İlgili görev: F11.

## DEC-014 - İki kişilik görev ayrımı

- Tarih: 2026-07-14
- Durum: `ONAYLANDI`
- Karar veren: Ürün sahibi
- Karar: Ali RAG/chatbot çekirdeğini; ikinci geliştirici platform/auth/admin/deployment
  işlerini yürütür. API, migration, entegrasyon ve yayın kararları ortaktır.
- Sonuç: `MASTER_PLAN.md` sorumluluk kodları bu ayrıma dayanır.

## DEC-015 - Sekiz haftalık beta hedefi kaliteyi geçersiz kılmaz

- Tarih: 2026-07-14
- Durum: `ONAYLANDI`
- Karar veren: Ürün sahibi ve teknik planlama
- Karar: 1-2 ay kapalı beta hazırlık hedefidir; kritik kalite kapısı geçilmezse yayın
  ertelenir, test/güvenlik kapsamı çıkarılmaz.
- Gerekçe: Takvim baskısının hukuki güveni düşürmesini engellemek.

## DEC-016 - Altyapı sağlayıcısı gereksinim ve maliyet sonrası seçilecek

- Tarih: 2026-07-14
- Durum: `ONAYLANDI`
- Karar veren: Ürün sahibi
- Karar: Şimdiden AWS/VPS/yönetilen servis kilidi yapılmaz. 20-100 kullanıcı için
  maliyet, bakım ve taşınabilirlik F13-01'de karşılaştırılır.
- İlgili görev: F12-05, F13-01.

## DEC-017 - Chatbot bitmeden yan modüller genişletilmeyecek

- Tarih: 2026-07-14
- Durum: `ONAYLANDI`
- Karar veren: Ürün sahibi ve teknik planlama
- Karar: Quiz, dashboard ve mevcut senaryo kodları korunur; chatbot beta kalite kapısını
  geciktirecek yeni özellik eklenmez.
- Gerekçe: İki kişilik ekibin odağını piyasaya çıkacak chatbotta tutmak.

## DEC-018 - Proje bir kerede yeniden yazılmayacak

- Tarih: 2026-07-14
- Durum: `ONAYLANDI`
- Karar veren: Teknik inceleme
- Karar: Test/baseline sonrası bağımsız parçalar kademeli değiştirilir; her adım tam
  regression ile karşılaştırılır.
- Gerekçe: Büyük yeniden yazımda hata kaynağını ve regression'ı izlemeyi kaybetmemek.
- Sonuç: Reference retrieval, reranker ve diğer stratejiler görev bazında geçer.
- İlgili belge: `ARCHITECTURE.md`.

## DEC-019 - F0-02 legacy depo temizliği uygulanacaktır

- Tarih: 2026-08-06
- Durum: `ONAYLANDI`
- Karar veren: Ürün sahibi ve teknik inceleme
- Karar: F0-02 kapsamında sınıflandırması ve ayrıntılı incelemesi tamamlanan 12
  gruptaki 21 legacy dosya depodan kaldırılır.
- Kaldırılan kapsam: Legacy `scenario_api.py` API akışı; yerel SQLite
  `data/hmgs.db`; eski Streamlit arayüzü; güncelliğini yitirmiş chatbot akış
  belgesi; eski quiz çalıştırıcısı; deneysel analiz betiği; eski seed ve veri
  yardımcıları; scratch senaryo betiği; legacy CLI raporlama betiği; eski SQL
  şemaları ve tablo oluşturma betiği; varsayılan Vite README ve görsel varlıkları;
  gereksiz `app/.gitkeep` placeholder dosyasıdır.
- Bağımlılık kanıtı: Kalan aktif kaynaklarda kaldırılan dosyalara yönelik import,
  çağrı, çalışma zamanı, build veya deployment bağımlılığı bulunmamıştır.
- Bağımlılık temizliği: Streamlit arayüzünün kaldırılmasıyla `requirements.txt`
  içindeki `streamlit` bağımlılığı da kaldırılmıştır.
- Depo koruması: Kök `.gitignore`; ortam varyantları, yerel DB, arşiv/yedek,
  test ve araç cache'i, editör ve geçici dosya desenleriyle güçlendirilmiştir.
- Kullanıcı dosyaları: `hmgs-ai-clean.zip` silinmemiş; diskte korunarak `*.zip`
  kuralıyla ignored yapılmıştır. `changes.txt`, `frontend/package-lock.json`,
  `retrieval/intent/candidates.py`, `retrieval/pipeline.py` ve
  `retrieval/scoring.py` korunmuş kullanıcı değişiklikleridir.
- Doğrulama: Yasaklı dosya ve hassas içerik taraması başarılıdır; tracked gerçek
  sır veya aktif legacy bağımlılığı bulunmamıştır.
- Sınır: Bu karar yalnızca F0-02 kapsamındadır ve F0-03'e geçiş anlamına gelmez.
- İlgili görev: F0-02.

## DEC-020 - Python 3.11 ve doğrudan bağımlılık pinleme standardı

- Tarih: 2026-08-14
- Durum: `ONAYLANDI`
- Karar veren: Ürün sahibi ve teknik inceleme
- Bağlam: F0-03 kapsamında backend'in yerel ortam kopyalanmadan temiz ve
  tekrar üretilebilir biçimde kurulması gerekir.
- Karar: Python 3.11.x kanonik geliştirme/çalışma serisi, Python 3.10 kaynak kodu
  sözdizimi alt sınırıdır. Doğrudan bağımlılıklar exact pinlenir; transitif
  bağımlılıklar doğrudan requirements listesine yazılmaz.
- Dosya yapısı: Production bağımlılıkları `requirements.txt`, development
  kurulumu `requirements-dev.txt` ile tanımlanır. Development dosyası bugün
  `-r requirements.txt` içerir.
- Kapsam sınırı: Pytest F1-02'ye, Alembic F2-02'ye ve izleme sağlayıcısı paketi
  F12'ye bırakılmıştır; bu paketler F0-03 kapsamında eklenmemiştir.
- Gerekçe: Yalnızca mevcut aktif kodun kanıtlanmış bağımlılıklarını sabitlemek ve
  gelecek görevlerin sağlayıcı/araç kararlarını erkenden kilitlememek.
- Sonuç: Temiz Python 3.11.5 ortamında production/development kurulumu ve backend
  import hedefi doğrulanabilir hale gelmiştir.
- İlgili görev/sorun: F0-03, ISSUE-003.

# Açık kararlar

## DEC-PENDING-001 - Kesin veri saklama süresi

- Durum: `ONERILDI`
- Gerekli olduğu görev: F11-01
- Seçenek: 30, 60 veya 90 gün; yasal/operasyonel gereksinimle kararlaştırılacak.

## DEC-PENDING-002 - Beta hosting sağlayıcısı

- Durum: `ONERILDI`
- Gerekli olduğu görev: F13-01
- Kriter: pgvector, backup, secret, monitoring, maliyet ve taşınabilirlik.

## DEC-PENDING-003 - Reranker üretimde kalacak mı?

- Durum: `ONERILDI`
- Gerekli olduğu görev: F6-03
- Kural: A/B evaluation kalite faydası gecikme/maliyeti haklı çıkarırsa kalır.

## DEC-PENDING-004 - Topic classifier kalacak mı?

- Durum: `ONERILDI`
- Gerekli olduğu görev: F6-02
- Kural: Metadata uyumu ve ablation faydası kanıtlanırsa kalır.
