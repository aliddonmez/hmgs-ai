# HMGS Chatbot - Bilinen Sorunlar

## Belge amacı

Bu belge kod incelemesi, testler, kullanıcı geri bildirimi ve üretim gözleminden bulunan
sorunların kanonik listesidir. Sorunlar sohbet mesajlarında bırakılmaz. Her sorun görev,
regression testi ve çözüm doğrulamasıyla ilişkilendirilir.

## Öncelik tanımları

- `P0`: Secret/veri sızıntısı, kritik güvenlik veya yayını durduran risk.
- `P1`: Yanlış hukuki cevap, yanlış kalite algısı, veri kaybı veya ana akış hatası.
- `P2`: Önemli sürdürülebilirlik, performans veya kullanıcı deneyimi sorunu.
- `P3`: Temizlik, dokümantasyon veya düşük riskli iyileştirme.

## Durumlar

- `ACIK`, `DEVAM_EDIYOR`, `BLOKE`, `COZULDU`, `KABUL_EDILDI`.

`COZULDU` durumu için çözüm commit'i ve geçen regression testi zorunludur.

# Açık sorunlar

## ISSUE-001 - API anahtarı örnek ve ortam dosyasında paylaşılmış

- Öncelik: `P0`
- Durum: `COZULDU`
- Alan: Güvenlik
- İlgili görev: F0-01
- Kanıt: `.env` ve `.env.example` içinde dolu Gemini anahtarı görüldü.
- Risk: Yetkisiz kullanım, maliyet ve hesap güvenliği.
- Çözüm: Açığa çıkan gizli değerler iptal edilip yenilendi; sabit kimlik bilgileri koddan kaldırıldı ve `.env.example` güvenli örnek değerlere dönüştürüldü.
- Çözüm commit'i: `fb71eb8`
- Regression: `TR-F0-01` - `BAŞARILI`
- Kapanış tarihi: `2026-07-27`

## ISSUE-002 - Proje arşivi bağımlılık ve gizli yerel dosyalar içeriyor

- Öncelik: `P1`
- Durum: `COZULDU`
- Alan: Depo hijyeni
- İlgili görev: F0-02
- Kanıt: `.venv`, `node_modules`, `.git`, ZIP, cache ve yerel DB dosyaları.
- Risk: Büyük depo, güvenlik sızıntısı ve tekrar üretilemeyen kurulum.
- Çözüm: 12 gruptaki 21 legacy dosya kaldırıldı; `.gitignore` genişletildi ve
  yasaklı dosya/hassas içerik taraması başarılı oldu.
- Çözüm commit'i: Bu kaydı içeren F0-02 kapanış commit'i.
- Regression: `TR-F0-02` - `BAŞARILI`
- Kapanış tarihi: `2026-08-06`

## ISSUE-003 - Python requirements aktif uygulamayı tam tanımlamıyor

- Öncelik: `P1`
- Durum: `ACIK`
- Alan: Kurulum
- İlgili görev: F0-03
- Kanıt: FastAPI, Uvicorn, Pydantic, pandas/plotly ve test araçları eksik.
- Risk: Yeni ortamda backend/Streamlit parçalarının çalışmaması.
- Çözüm: Aktif ürün bağımlılıklarını sürümlü ve ayrılmış biçimde tanımlamak.

## ISSUE-004 - Frontend lock dosyası package.json ile uyumsuz

- Öncelik: `P1`
- Durum: `ACIK`
- Alan: Frontend kurulum
- İlgili görev: F0-04
- Kanıt: `npm ci` EUSAGE/eksik bağımlılık hatasıyla durdu.
- Risk: CI ve temiz production build yapılamaz.

## ISSUE-005 - Intent test runner v4 ve v5 için yanlış dosyaları yüklüyor

- Öncelik: `P1`
- Durum: `ACIK`
- Alan: Test doğruluğu
- İlgili görev: F1-01
- Kanıt: v4 -> v2, v5 -> v3 import ediliyor.
- Risk: 300/300 şeklinde yanlış kalite algısı.
- Regression: Her sürümün kaynak modül/benzersiz vaka ID testi.

## ISSUE-006 - Gerçek v5 Intent sonucu 45/60

- Öncelik: `P1`
- Durum: `ACIK`
- Alan: Intent/target extraction
- İlgili görev: F4-02
- Kanıt: Gerçek `test_cases_v5.py` doğrudan çalıştırıldı.
- Risk: Çoklu tanım soruları single-focus retrieval'a gider.
- Kök neden adayı: Relation marker sonrası kalan iki kavram tek phrase target oluyor.
- Çözüm sınırı: Sorulara özel kavram keyword'ü eklenmeyecek.

## ISSUE-007 - Retrieval evaluation ürün hedefini yanlış modelliyor

- Öncelik: `P1`
- Durum: `ACIK`
- Alan: Evaluation
- İlgili görev: F1-03, F1-04
- Kanıt: Comparison soruları çoklu gerekli madde yerine `uncertain` bekliyor.
- Risk: Doğru retrieval başarısız, yanlış davranış başarılı sayılabilir.

## ISSUE-008 - Kayıtlı retrieval sonucu %55

- Öncelik: `P1`
- Durum: `ACIK`
- Alan: Retrieval kalitesi
- İlgili görev: F5-F6
- Kanıt: 22/40 kayıtlı evaluation sonucu.
- Not: Evaluation şeması hatalı olduğu için kanonik baseline değildir.
- Risk: Yanlış veya eksik TCK maddesiyle cevap üretimi.

## ISSUE-009 - Reference intent doğrudan madde lookup kullanmıyor

- Öncelik: `P1`
- Durum: `ACIK`
- Alan: Retrieval mimarisi
- İlgili görev: F5-01
- Kanıt: Bütün non-comparison sorgular `vector_search(expanded_query)` yoluna gider.
- Risk: Kullanıcının açıkça istediği madde yerine semantic komşu madde gelebilir.

## ISSUE-010 - Query expansion bileşik suç sorgusunu bozabiliyor

- Öncelik: `P1`
- Durum: `ACIK`
- Alan: Retrieval/query expansion
- İlgili görev: F5-06
- Kanıt: `taksirle öldürme` sorgusunda TCK 85 yerine TCK 22 üst sıraya çıktı.
- Risk: Ana suç başlığı yerine genel kavram maddesi seçilir.

## ISSUE-011 - Topic classifier metadata ile uyumsuz ve çoğunlukla etkisiz

- Öncelik: `P2`
- Durum: `ACIK`
- Alan: Retrieval/scoring
- İlgili görev: F6-02
- Kanıt: Classifier dört topic üretirken TCK document `konu=Genel` taşıyor; topic boost
  çoğu evaluation çıktısında 0.
- Risk: Gereksiz karmaşıklık ve yanlış güven.
- Çözüm: Metadata taksonomisiyle uyum veya ölçülmüş fayda yoksa kaldırma.

## ISSUE-012 - Reranker guardrail yanlış skor alanını kullanıyor

- Öncelik: `P1`
- Durum: `ACIK`
- Alan: Reranking
- İlgili görev: F6-01
- Kanıt: `rerank_score = c.get("score", 0)` eski vector skorunu okuyor.
- Risk: Guardrail amaçlandığı gibi çalışmaz.

## ISSUE-013 - Reranker sırası final_score ile yeniden bozuluyor

- Öncelik: `P1`
- Durum: `ACIK`
- Alan: RAG orkestrasyonu
- İlgili görev: F6-01
- Kanıt: Reranker sonrası `app/rag_pipeline.py` tekrar `final_score` ile sıralıyor.
- Risk: Reranker gecikme üretir fakat context sırasına fiilen etki etmez.

## ISSUE-014 - Scoring aynı lexical sinyali birden fazla kez ödüllendirebilir

- Öncelik: `P1`
- Durum: `ACIK`
- Alan: Scoring
- İlgili görev: F6-02
- Kanıt: Title, exact title, target, search target ve lexical boost örtüşebilir.
- Risk: Kalibre edilemeyen 1.0 üstü skor ve yanlış sıralama.

## ISSUE-015 - Retrieval eşikleri confidence gibi kullanılıyor

- Öncelik: `P1`
- Durum: `ACIK`
- Alan: Answer/no-answer
- İlgili görev: F6-04
- Kanıt: Elle ağırlıklandırılmış final skor üzerinde sabit top/avg/margin eşikleri.
- Risk: Yanlış cevap veya gereksiz ret.

## ISSUE-016 - Kapsam dışı kontrol birkaç sabit kelimeye bağlı

- Öncelik: `P1`
- Durum: `ACIK`
- Alan: Safety/scope
- İlgili görev: F4-01, F6-04
- Kanıt: `ofsayt`, `futbol`, `kahve`, `python` gibi sınırlı liste.
- Risk: TCK dışı veya kişisel danışmanlık sorusu cevaplanabilir.

## ISSUE-017 - Tek prompt bütün soru türlerinde kullanılıyor

- Öncelik: `P2`
- Durum: `ACIK`
- Alan: Generation
- İlgili görev: F7-01
- Risk: Reference, comparison ve scenario cevap biçimleri güvenilir ayrışmaz.

## ISSUE-018 - Gemini hata metni başarılı answer sayılabilir

- Öncelik: `P1`
- Durum: `ACIK`
- Alan: LLM hata yönetimi
- İlgili görev: F7-04
- Kanıt: Client exception yerine `LLM hata verdi.` döndürüyor; üst katman uzunluk
  kontrolünden geçirip answer kabul edebilir.
- Risk: Teknik hata kullanıcıya chatbot cevabı olarak gösterilir.

## ISSUE-019 - Citation validation bulunmuyor

- Öncelik: `P1`
- Durum: `ACIK`
- Alan: Hukuki cevap güvenliği
- İlgili görev: F7-03
- Risk: Gemini retrieval context dışında madde numarası veya iddia üretebilir.

## ISSUE-020 - Embedding modeli ortam dosyalarında tutarsız

- Öncelik: `P1`
- Durum: `ACIK`
- Alan: Embedding/index
- İlgili görev: F2-04
- Kanıt: Multilingual model ve all-MiniLM modeli farklı yerlerde tanımlı.
- Risk: Boyut aynı olduğu halde farklı embedding uzayı sessiz kalite kaybı yaratır.

## ISSUE-021 - Birden fazla ve çakışan DB şema kaynağı var

- Öncelik: `P1`
- Durum: `ACIK`
- Alan: Veritabanı
- İlgili görev: F2-01-F2-03
- Kanıt: `schema.sql`, `full_db.sql`, create scriptleri ve runtime `CREATE TABLE`.
- Risk: Kolon hatası, veri kaybı ve ortamlar arası farklı davranış.

## ISSUE-022 - Uygulama request sırasında tablo oluşturmaya çalışıyor

- Öncelik: `P2`
- Durum: `ACIK`
- Alan: Veritabanı yaşam döngüsü
- İlgili görev: F2-02
- Kanıt: Profil/attempt/scenario çağrıları `init_storage` çalıştırıyor.
- Risk: Yetki, latency ve migration kontrolü sorunu.

## ISSUE-023 - PostgreSQL bağlantı kodu birçok yerde tekrar ediliyor

- Öncelik: `P2`
- Durum: `ACIK`
- Alan: Veri erişimi
- İlgili görev: F12-03
- Risk: Tutarsız timeout/pool ve bakım maliyeti.

## ISSUE-024 - Kullanıcı authentication ve veri izolasyonu yok

- Öncelik: `P1`
- Durum: `ACIK`
- Alan: Ürün güvenliği
- İlgili görev: F9-02, F9-03
- Kanıt: Kullanıcı serbest metin `user_id` seçiyor.
- Risk: Başka kullanıcının verisine erişim.

## ISSUE-025 - Quiz session'ları yalnızca process RAM'inde

- Öncelik: `P2`
- Durum: `ACIK`
- Alan: Mevcut yan modül
- İlgili görev: Chatbot kritik yolunun dışında; karar kaydı gerekli.
- Risk: Restart ve multi-worker ortamında session kaybı.

## ISSUE-026 - Health endpoint gerçek bağımlılıkları kontrol etmiyor

- Öncelik: `P2`
- Durum: `ACIK`
- Alan: Operasyon
- İlgili görev: F9-05
- Kanıt: Yalnızca `{status: ok}` döndürüyor.
- Risk: DB/model hazır değilken trafik alınır.

## ISSUE-027 - Merkezi yapılandırılmış logging ve tracing yok

- Öncelik: `P2`
- Durum: `ACIK`
- Alan: Gözlemlenebilirlik
- İlgili görev: F12-01, F12-02
- Kanıt: Retrieval boyunca doğrudan `print` debug çıktıları.
- Risk: Üretim hatası ve latency kök nedeni bulunamaz; içerik log sızıntısı olabilir.

## ISSUE-028 - ScenarioPage sabit localhost API adresi kullanıyor

- Öncelik: `P2`
- Durum: `ACIK`
- Alan: Frontend config
- İlgili görev: F0-04
- Risk: Production ortamında scenario istekleri yanlış adrese gider.

## ISSUE-029 - Legacy scenario_api sabit DB bilgisi ve açık CORS içeriyor

- Öncelik: `P1`
- Durum: `COZULDU`
- Alan: Legacy/güvenlik
- İlgili görev: F0-02
- Risk: Yanlışlıkla çalıştırılırsa güvensiz ikinci API yüzeyi oluşur.
- Çözüm: Aktif FastAPI uygulamasında karşılığı olmayan legacy `scenario_api.py`
  kaldırıldı; kalan tracked aktif kaynaklarda import, çağrı veya deployment
  bağımlılığı bulunmadığı doğrulandı.
- Çözüm commit'i: Bu kaydı içeren F0-02 kapanış commit'i.
- Regression: `TR-F0-02` - `BAŞARILI`
- Kapanış tarihi: `2026-08-06`

## ISSUE-030 - README ve eski aktif akış belgesi güncel değil

- Öncelik: `P3`
- Durum: `ACIK`
- Alan: Dokümantasyon
- İlgili görev: Takip belgeleri ve sonraki kurulum görevi
- Kanıt: README üç satır; eski flow Intent Engine'i içermiyor.
- Risk: Yeni sohbet/geliştirici yanlış dosyada çalışabilir.

# Sorun kapatma şablonu

Bir sorun çözüldüğünde kayda şu alanlar eklenir:

```text
Durum: COZULDU
Çözüm görevi:
Commit:
Regression test ID:
Test run ID:
Çözüm özeti:
Kalan risk:
```

Sorun kaydı silinmez. Böylece geçmişte hangi mimari hataların neden ve nasıl
çözüldüğü izlenebilir.
