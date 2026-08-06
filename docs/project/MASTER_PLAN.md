# HMGS Chatbot - Ana Geliştirme Planı

## Belge amacı

Bu belge, HMGS TCK chatbotunu kapalı betaya ve ardından herkese açık yayına
hazırlamak için uygulanacak kanonik iş planıdır. Ürün kapsamı
`PRODUCT_SCOPE.md` tarafından belirlenir. Bu plan sohbet geçmişinden bağımsız
olarak projenin hangi sırayla geliştirileceğini, her görevin nasıl test
edileceğini ve ne zaman tamamlanmış sayılacağını tanımlar.

## Durum değerleri

- `BEKLIYOR`: Çalışma başlamadı.
- `HAZIR`: Bağımlılıklar tamamlandı, başlanabilir.
- `DEVAM_EDIYOR`: Aktif çalışma var.
- `BLOKE`: Harici karar veya eksik bağımlılık var.
- `INCELEME`: Kod tamamlandı, test veya inceleme bekliyor.
- `TAMAMLANDI`: Zorunlu testler ve çıkış kriterleri geçti.

Bir görev yalnızca kod yazıldığı için `TAMAMLANDI` yapılamaz. Görevin altında
tanımlanan doğrulamalar çalıştırılmalı ve sonuç `TEST_RESULTS.md` içinde
kaydedilmelidir.

## Sorumluluk kodları

- `RAG`: Ali - chatbot, intent, retrieval, reranker, prompt ve evaluation.
- `PLATFORM`: İkinci geliştirici - auth, yönetici paneli, deployment ve izleme.
- `ORTAK`: API, migration, entegrasyon, güvenlik ve yayın kararları.
- `HUKUK`: Beta öncesi örnek cevapları inceleyecek hukuk alanı uzmanı.

## Değişmez çalışma döngüsü

Her görevde aşağıdaki sıra uygulanır:

1. Aktif branch ve görev kodu doğrulanır.
2. Görev öncesi ilgili testler çalıştırılır ve baseline kaydedilir.
3. Başarısız davranış mümkünse yeni bir regression testiyle yeniden üretilir.
4. Genel mimari çözüm geliştirilir.
5. Göreve özel unit ve integration testleri çalıştırılır.
6. Tam regression paketi çalıştırılır.
7. Önceki baseline ile kalite, gecikme ve maliyet farkı karşılaştırılır.
8. Bozulma varsa görev tamamlanmaz.
9. Belgeler ve `CURRENT_STATUS.md` güncellenir.
10. Değişiklik incelemeye ve commit'e hazır hale getirilir.

## Kapsam koruma kuralları

- Tek bir soruyu düzeltmek için soruya özel keyword eklenmez.
- Bir mimari hata yalnızca scoring katsayısıyla gizlenmez.
- Test setindeki ifadeler üretim kuralı olarak kopyalanmaz.
- Model değiştiğinde eski embedding'ler kullanılmaz.
- Retrieval, generation ve cevap verme kararı ayrı ölçülür.
- Kullanıcı geri bildirimi doğrulanmadan otomatik kurala dönüşmez.
- Her fazın kalite kapısı geçilmeden sonraki bağımlı faz tamamlanmış sayılmaz.
- Quiz, dashboard ve mevcut senaryo özellikleri chatbot kalite kapısını
  geciktirecek biçimde genişletilmez.

# Zaman ve sürüm hedefleri

## Ana hedef

- Geliştirme dönemi: 8 hafta.
- İlk yayın: 20-100 kullanıcıyla kapalı beta.
- Beta gözlem dönemi: En az 2 hafta.
- Herkese açık yayın: Beta verileri ve yayın kapıları geçildikten sonra.

Sekiz hafta katı teslim garantisi değildir. Kritik güvenlik veya doğruluk kapısı
geçilmezse kapsam genişletilmez ve yayın tarihi kalite uğruna ertelenir.

# FAZ 0 - Güvenli ve tekrar üretilebilir proje tabanı

## F0-01 - Açığa çıkan anahtarları iptal et ve yenile

- Durum: `TAMAMLANDI`
- Sorumlu: `ORTAK`
- Bağımlılık: Yok
- Tahmin: 0.5 gün

Yapılacaklar:

- Paylaşılmış Gemini anahtarı iptal edilir.
- Yeni anahtar yalnızca yerel/üretim secret yönetimine kaydedilir.
- `.env.example` içindeki gerçek görünümlü değerler boş örneğe çevrilir.
- Git geçmişinde secret taraması yapılır.
- Gerekirse geçmiş temizliği ve anahtar rotasyonu tamamlanır.

Zorunlu testler:

- Secret scanner depo üzerinde çalışır.
- `.env` Git tarafından izlenmez.
- Eksik anahtarda uygulama kontrollü ve gizli değer sızdırmadan hata verir.

Tamamlanma kriteri:

- Aktif anahtarın hiçbir Git commit'inde veya örnek dosyada bulunmadığı doğrulanır.

## F0-02 - Depo ve legacy dosya temizliği

- Durum: `TAMAMLANDI`
- Sorumlu: `ORTAK`
- Bağımlılık: F0-01
- Tahmin: 0.5 gün

Yapılacaklar:

- `.venv`, `node_modules`, cache, ZIP, yerel DB ve işletim sistemi artıkları
  depodan çıkarılır.
- Aktif, legacy ve deneysel dosyalar sınıflandırılır.
- `scenario_api.py`, eski SQLite akışı ve çakışan scriptler için kaldırma/legacy
  kararı `DECISIONS.md` içine yazılır.
- `.gitignore` güncellenir.

Zorunlu testler:

- Yasaklı dosya desenleri için depo taraması.
- Aktif modüllerde legacy import bulunmadığının kontrolü.

Tamamlanma kriteri:

- Kaynak depo yeniden üretilemeyen yerel bağımlılık ve gizli veri içermez.

## F0-03 - Python bağımlılıklarını standardize et

- Durum: `BEKLIYOR`
- Sorumlu: `ORTAK`
- Bağımlılık: F0-02
- Tahmin: 0.5 gün

Yapılacaklar:

- Eksik FastAPI, Uvicorn, test, migration ve izleme bağımlılıkları eklenir.
- Sürümler kontrollü biçimde sabitlenir.
- Python sürümü belgelenir.
- Üretim ve geliştirme bağımlılıkları ayrılır.

Zorunlu testler:

- Temiz virtualenv içinde kurulum.
- Bütün aktif Python modüllerinin import smoke testi.
- `python -m compileall` kontrolü.

Tamamlanma kriteri:

- Yeni bilgisayarda yerel ortam kopyalanmadan backend kurulabilir.

## F0-04 - Frontend bağımlılıklarını standardize et

- Durum: `BEKLIYOR`
- Sorumlu: `PLATFORM`
- Bağımlılık: F0-02
- Tahmin: 0.5 gün

Yapılacaklar:

- `package.json` ile lock dosyası senkronize edilir.
- Sabit localhost API adresleri merkezi config'e taşınır.

Zorunlu testler:

- `npm ci`
- `npm run lint`
- `npm run build`

Tamamlanma kriteri:

- Frontend temiz kurulum ve production build'i hatasız tamamlar.

## F0-05 - CI başlangıç hattını kur

- Durum: `BEKLIYOR`
- Sorumlu: `PLATFORM`
- Bağımlılık: F0-03, F0-04
- Tahmin: 1 gün

Yapılacaklar:

- Python test, lint, compile ve secret scan işleri eklenir.
- Frontend lint ve build işleri eklenir.
- Başarısız kontrolde merge engellenir.

Zorunlu testler:

- Bilerek bozulan testin CI'ı durdurması.
- Başarılı branch'in bütün işleri geçmesi.

Tamamlanma kriteri:

- Temel kalite kontrolleri otomatik çalışmadan kod birleştirilemez.

### Faz 0 kalite kapısı

- Temiz backend kurulumu başarılı.
- Temiz frontend kurulumu başarılı.
- Secret taraması başarılı.
- CI zorunlu kontrolleri başarılı.

# FAZ 1 - Güvenilir test ve evaluation temeli

## F1-01 - Intent test runner v4/v5 hatasını düzelt

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F0-03
- Tahmin: 0.25 gün

Yapılacaklar:

- v4 ve v5 doğru test modüllerini yükler.
- Sürüm-test dosyası eşleşmesi tek yerde tanımlanır.

Zorunlu testler:

- Her sürümün benzersiz vaka ID'lerinin raporlanması.
- v1-v5'in gerçekten ayrı dosyalardan geldiğinin testi.

Tamamlanma kriteri:

- Gerçek başlangıç sonucu yeniden üretilebilir; mevcut incelemede beklenen sonuç
  yaklaşık 285/300'dür.

## F1-02 - Intent testlerini pytest'e taşı

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F1-01
- Tahmin: 1 gün

Yapılacaklar:

- Bütün vakalara benzersiz ID eklenir.
- Intent, relation, target count ve target exact match ayrı assertion olur.
- Tek vaka ve tek set çalıştırma desteği eklenir.

Zorunlu testler:

- 300 vakanın parametrik çalışması.
- Yinelenen ID ve yinelenen soru kontrolü.
- Hatalı beklenen sonuç şemasının testi durdurması.

Tamamlanma kriteri:

- Intent regression paketi tek komutla ve makine okunabilir raporla çalışır.

## F1-03 - Retrieval evaluation şemasını yenile

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F1-02
- Tahmin: 1 gün

Yapılacaklar:

- Tek `expected_madde` yerine `required_articles`, `acceptable_articles`,
  `forbidden_articles` ve `should_answer` alanları kullanılır.
- Comparison vakaları birden fazla gerekli maddeyle ölçülür.
- Soru türü ve zorluk etiketi eklenir.

Zorunlu testler:

- Hatalı evaluation kaydı şema doğrulamasından geçemez.
- Çoklu kaynak başarı/başarısızlık örnekleri unit testle doğrulanır.

Tamamlanma kriteri:

- Reference, single, comparison, scenario ve no-answer vakaları aynı raporda
  doğru metriklerle ölçülebilir.

## F1-04 - RAG metrik motorunu oluştur

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F1-03
- Tahmin: 1 gün

Yapılacaklar:

- Recall@1/3/5, Precision@K, MRR, NDCG ve target coverage hesaplanır.
- Answer/no-answer confusion matrix oluşturulur.
- Soru türü bazında sonuç üretilir.

Zorunlu testler:

- Küçük yapay veri üzerinde her metrik için bilinen sonuç testi.
- Boş sonuç ve çoklu doğru kaynak edge case testleri.

Tamamlanma kriteri:

- Aynı evaluation girdisi her çalışmada aynı metrikleri üretir.

## F1-05 - Başlangıç baseline raporunu kaydet

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F1-04
- Tahmin: 0.5 gün

Yapılacaklar:

- Kod değiştirilmeden intent ve retrieval sonuçları kaydedilir.
- Ortalama/P95 süre, cevap verme oranı ve hata listesi çıkarılır.
- Çalışma commit'i, model ve DB sürümü rapora eklenir.

Zorunlu testler:

- Aynı ortamda iki koşunun tolerans dahilinde tutarlılığı.
- Raporun eksik model/DB sürümünü reddetmesi.

Tamamlanma kriteri:

- Sonraki bütün RAG değişiklikleriyle karşılaştırılacak kanonik baseline vardır.

### Faz 1 kalite kapısı

- Test vakalarının gerçek dosya eşleşmesi doğrulanmış.
- Intent ve retrieval ayrı ölçülüyor.
- Soru türü bazında baseline kayıtlı.
- Test ve tuning setlerini ayırma kuralı belgelenmiş.

# FAZ 2 - Kanonik veritabanı ve sürümlü içerik modeli

## F2-01 - Hedef veri modelini tasarla

- Durum: `BEKLIYOR`
- Sorumlu: `ORTAK`
- Bağımlılık: F1-05
- Tahmin: 1 gün

Yapılacaklar:

- Kaynak, belge, sürüm, hukuki birim, chunk ve embedding tabloları tasarlanır.
- Chat session, message, feedback ve evaluation tabloları modellenir.
- TCK'ya özel kolonlar yerine genişletilebilir hukuki metadata kullanılır.

Zorunlu testler:

- Örnek TCK maddesi, fıkra ve bent verisinin modele kayıpsız eşlenmesi.
- Birden fazla belge sürümünün birlikte tutulması.

Tamamlanma kriteri:

- ER modeli incelenmiş ve `DECISIONS.md` içinde onaylanmıştır.

## F2-02 - Alembic migration altyapısını kur

- Durum: `BEKLIYOR`
- Sorumlu: `PLATFORM`
- Bağımlılık: F2-01
- Tahmin: 1 gün

Yapılacaklar:

- İlk kanonik migration oluşturulur.
- Uygulama içindeki tablo oluşturma kodları kaldırılacak şekilde planlanır.

Zorunlu testler:

- Boş DB'ye upgrade.
- Downgrade ve tekrar upgrade.
- Migration'ın ikinci kez güvenli çalışması.

Tamamlanma kriteri:

- Şema yalnızca migration sistemiyle yönetilir.

## F2-03 - Eski veriyi yeni şemaya taşı

- Durum: `BEKLIYOR`
- Sorumlu: `ORTAK`
- Bağımlılık: F2-02
- Tahmin: 1 gün

Yapılacaklar:

- Eski `documents`, `document_chunks`, soru ve profil verileri için taşıma yazılır.
- Veri kaybı kontrolü yapılır.

Zorunlu testler:

- Satır sayısı, hash ve örnek içerik karşılaştırması.
- Taşıma yarıda kesildiğinde tekrar çalıştırma.
- Eski şema varyantları için fixture testleri.

Tamamlanma kriteri:

- Aktif geliştirme verisi kanonik şemada çalışır.

## F2-04 - Embedding uyumluluk koruması ekle

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F2-02
- Tahmin: 0.5 gün

Yapılacaklar:

- Model adı, sürüm, boyut, normalization ve chunking sürümü kaydedilir.
- Sorgu modeli ile indeks modeli uyuşmazsa arama engellenir.

Zorunlu testler:

- Aynı boyutlu fakat farklı model uyuşmazlığı.
- Farklı boyut testi.
- Doğru modelle başarılı retrieval.

Tamamlanma kriteri:

- Eski ve yeni embedding uzayları yanlışlıkla karıştırılamaz.

### Faz 2 kalite kapısı

- Tek kanonik şema ve migration kaynağı var.
- Eski veri kontrollü taşınabiliyor.
- Belge ve embedding sürümleri izlenebilir.

# FAZ 3 - Güvenilir TCK ingest ve güncelleme sistemi

## F3-01 - TCK parser fixture setini oluştur

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F2-04
- Tahmin: 1 gün

Yapılacaklar:

- Normal, uzun, bentli, geçici, mülga ve değişiklik notlu madde örnekleri hazırlanır.
- PDF metin bozulmaları fixture olarak eklenir.

Zorunlu testler:

- Madde/fıkra/bent sınırı exact match.
- Sayfa başlığı ve satır bölünmesi temizliği.

Tamamlanma kriteri:

- Parser değişikliği sabit bir regression setiyle ölçülür.

## F3-02 - Parser ve deterministik chunking'i güçlendir

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F3-01
- Tahmin: 1.5 gün

Yapılacaklar:

- Madde hiyerarşisi korunur.
- Uzun madde fıkra/bent sınırında bölünür.
- Her chunk üst madde metadata'sını taşır.

Zorunlu testler:

- Chunk tekrarları ve kayıp metin kontrolü.
- Birleştirilen chunk'ların normalize kaynak metni yeniden oluşturması.
- Aynı girdinin aynı chunk'ları üretmesi.

Tamamlanma kriteri:

- Chunking deterministik ve hukuki yapı farkındalıklıdır.

## F3-03 - TCK ingest'i idempotent hale getir

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F3-02
- Tahmin: 0.5 gün

Yapılacaklar:

- Aynı dosya yeniden işlendiğinde gereksiz sürüm ve embedding oluşmaz.
- Başarısız ingest aktif sürümü etkilemez.

Zorunlu testler:

- Aynı dosyayı iki kez ingest.
- Yarıda kalan transaction.
- Bozuk/eksik dosya.

Tamamlanma kriteri:

- Ingest tekrar çalıştırılabilir ve atomiktir.

## F3-04 - Mevzuat değişiklik algılama ve onay akışını kur

- Durum: `BEKLIYOR`
- Sorumlu: `ORTAK`
- Bağımlılık: F3-03
- Tahmin: 1.5 gün

Yapılacaklar:

- Resmî kaynak hash kontrolü yapılır.
- Madde bazında eski-yeni fark üretilir.
- Aday sürüm yönetici onayı bekler.
- Onay sonrası indekslenir ve aktif edilir.
- Rollback desteklenir.

Zorunlu testler:

- Değişiklik yok, madde ekleme, değiştirme, kaldırma ve mülga senaryoları.
- Başarısız indeksleme.
- Eski sürüme rollback.

Tamamlanma kriteri:

- Onaysız TCK sürümü kullanıcı cevaplarında kullanılamaz.

### Faz 3 kalite kapısı

- Kaynak metin kaybı ve chunk tekrarı yok.
- Her cevapta kullanılan TCK sürümü izlenebilir.
- Güncelleme ve rollback test edilmiştir.

# FAZ 4 - Intent Engine 2.0 ve konuşma çözümleme

## F4-01 - Intent sözleşmesini standardize et

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F1-05
- Tahmin: 0.5 gün

Yapılacaklar:

- `reference_lookup`, `single_concept`, `comparison`, `topic_explanation`,
  `scenario_analysis`, `follow_up`, `unsupported_legal`, `out_of_scope` ve
  `clarification_needed` türleri tanımlanır.
- Çıktı şeması Pydantic/dataclass ile doğrulanır.

Zorunlu testler:

- Eksik ve geçersiz intent çıktılarının reddedilmesi.

Tamamlanma kriteri:

- Retrieval katmanı tek ve sürümlü intent sözleşmesi tüketir.

## F4-02 - Multi-definition target extraction'ı düzelt

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F4-01
- Tahmin: 1 gün

Yapılacaklar:

- `kast taksir nedir` benzeri sorgular genel dil sinyalleriyle ayrıştırılır.
- Test sorularına özel kavram listesi çözüm olarak kullanılmaz.

Zorunlu testler:

- Mevcut v5 başarısız 15 vaka regression testi.
- Daha önce başarılı v1-v4 tam regression.
- Görülmemiş yeni iki/üç hedefli vakalar.

Tamamlanma kriteri:

- Yeni çözüm eski başarılı grupları bozmaz ve target exact match'i yükseltir.

## F4-03 - Reference extraction'ı sağlamlaştır

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F4-01
- Tahmin: 0.5 gün

Yapılacaklar:

- Farklı madde yazımları ve birden fazla madde desteklenir.
- Yıl, ceza süresi ve madde numarası birbirinden ayrılır.

Zorunlu testler:

- `TCK 141`, `141. madde`, `m. 141`, `141 ve 142. maddeler`.
- Madde olmayan sayılar.

Tamamlanma kriteri:

- Article extraction test doğruluğu beta hedefi olan %99'a ulaşır.

## F4-04 - Intent güven ve açıklama isteme politikasını kur

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F4-02, F4-03
- Tahmin: 0.5 gün

Yapılacaklar:

- Sabit confidence değerleri yerine sinyal tabanlı güven üretilir.
- Düşük güvenli ve çelişkili sorularda clarification kararı verilir.

Zorunlu testler:

- Sınır değerleri, çelişkili marker'lar ve eksik hedefler.

Tamamlanma kriteri:

- Düşük güvenli soru sessizce yanlış retrieval stratejisine gönderilmez.

### Faz 4 kalite kapısı

- Genel intent doğruluğu en az %95.
- Reference extraction en az %99.
- Comparison target exact match en az %95.
- Önceki başarılı test gruplarında kritik regression yok.

# FAZ 5 - Intent-aware retrieval

## F5-01 - Reference retrieval geliştir

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F3-04, F4-03
- Tahmin: 0.5 gün

Yapılacaklar:

- Açık madde sorgusu embedding yerine doğrudan metadata lookup kullanır.
- İstenen madde/fıkra kapsamı korunur.

Zorunlu testler:

- Var olan, olmayan, mülga ve çoklu madde sorguları.
- Yanlış komşu madde getirmeme testi.

Tamamlanma kriteri:

- Açık ve geçerli madde sorgularında yaklaşık %100 doğru kaynak.

## F5-02 - Single-concept retrieval geliştir

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F5-01
- Tahmin: 1 gün

Yapılacaklar:

- Başlık/metadata ve semantic adaylar birlikte ama ayrı sinyallerle kullanılır.
- Bileşik suç adı korunur.

Zorunlu testler:

- Basit/nitelikli suç, kast/taksir ve yakın başlık vakaları.

Tamamlanma kriteri:

- Single-concept Recall@5 en az %90 ve baseline'dan kötü değildir.

## F5-03 - Comparison retrieval geliştir

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F5-02, F4-02
- Tahmin: 1 gün

Yapılacaklar:

- Her hedef bağımsız aranır.
- Kaynaklar hedef bazında dengelenir.
- Her hedef için coverage raporlanır.

Zorunlu testler:

- İki ve üç hedefli karşılaştırmalar.
- Bir hedefin diğerini bastırmaması.
- Olası kast/bilinçli taksir ve yağma/hırsızlık regression'ları.

Tamamlanma kriteri:

- Gerekli bütün maddeleri bulma oranı en az %90.

## F5-04 - Topic explanation retrieval geliştir

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F5-02
- Tahmin: 0.75 gün

Yapılacaklar:

- Tek top chunk yerine gerekli madde grubunu kapsayan kaynak seçilir.
- TCK'da açıklanmayan doktrinsel boşluklar işaretlenir.

Zorunlu testler:

- Çok maddeli konu, kaynakta olmayan teori ve gereksiz madde yayılımı.

Tamamlanma kriteri:

- Kaynak kapsamı yeterli değilse sistem cevap yerine sınırlama üretir.

## F5-05 - Scenario retrieval geliştir

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F5-02
- Tahmin: 1 gün

Yapılacaklar:

- Fiil, netice, kast/taksir, rıza, mal ve cebir/tehdit gibi ayırt edici
  unsurlar yapılandırılmış sorguya dönüştürülür.
- Somut hukuki danışmanlık ile eğitim senaryosu sınırı uygulanır.

Zorunlu testler:

- Kısa/uzun senaryo, gereksiz ayrıntı ve yetersiz olay bilgisi.

Tamamlanma kriteri:

- Scenario Recall@5 en az %90; belirsiz olayda clarification/no-answer çalışır.

## F5-06 - Query expansion'ı hedef farkındalıklı yap

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F5-02, F5-03
- Tahmin: 0.75 gün

Yapılacaklar:

- Ek terimler ana sorgudan ayrı tutulur ve ölçülür.
- `taksirle öldürme` gibi bileşik başlıklar bozulmaz.
- Fayda sağlamayan expansion kapatılabilir olur.

Zorunlu testler:

- Expansion açık/kapalı A/B evaluation.
- Bileşik suç regression seti.

Tamamlanma kriteri:

- Expansion genel metriği veya hedeflenen grubu ölçülebilir biçimde iyileştirir;
  iyileştirmiyorsa üretim akışına alınmaz.

### Faz 5 kalite kapısı

- Her intent için açık retrieval stratejisi var.
- Soru türü bazında Recall@5 en az %90.
- Comparison gerekli kaynak kapsamı en az %90.
- Reference lookup yaklaşık %100.

# FAZ 6 - Skor, reranker ve cevap verme eşikleri

## F6-01 - Reranker entegrasyon hatalarını düzelt

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F5-06
- Tahmin: 0.5 gün

Yapılacaklar:

- Guardrail gerçek `rerank_score` kullanır.
- Reranker sırası sonradan eski `final_score` ile bozulmaz.
- Önce/sonra sıralamalar gözlemlenebilir olur.

Zorunlu testler:

- Rerank skor alanı ve sıralama unit testi.
- Bilinen aday listesinde beklenen sıra.

Tamamlanma kriteri:

- Reranker çıktısı bağlam seçimine fiilen etki eder.

## F6-02 - Scoring sinyallerini sadeleştir

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F6-01
- Tahmin: 1 gün

Yapılacaklar:

- Aynı lexical sinyali tekrar ödüllendiren bileşenler belirlenir.
- Skor açıklanabilir bileşenlere indirgenir.
- Intent'e özel scoring ihtiyacı değerlendirilir.

Zorunlu testler:

- Her skor bileşeni için unit test.
- Ablation evaluation: her sinyal kapatıldığında etki.

Tamamlanma kriteri:

- Kalan her skor sinyalinin ölçülmüş faydası veya açık guardrail görevi vardır.

## F6-03 - Reranker A/B değerlendirmesi yap

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F6-02
- Tahmin: 0.5 gün

Yapılacaklar:

- Kapalı/açık retrieval kalitesi, gecikme ve bellek karşılaştırılır.

Zorunlu testler:

- Tam evaluation seti iki modda çalışır.
- P50/P95 süre ve kaynak kullanımı kaydedilir.

Tamamlanma kriteri:

- Reranker yalnızca net fayda sağlıyorsa üretimde kalır.

## F6-04 - Answer/no-answer eşiklerini kalibre et

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F6-03
- Tahmin: 1 gün

Yapılacaklar:

- Global skorların confidence olmadığı kabul edilerek threshold sweep yapılır.
- Intent'e özel eşikler değerlendirilir.

Zorunlu testler:

- False-answer ve false-refusal confusion matrix.
- Eşik sınır değer testleri.

Tamamlanma kriteri:

- Seçilen eşikler evaluation raporuyla gerekçelendirilir.

### Faz 6 kalite kapısı

- Reranker etkisi ölçülmüş.
- Scoring bileşenleri gerekçeli.
- Answer/no-answer politikası test verisiyle kalibre.
- Genel retrieval beta hedefi en az %90.

# FAZ 7 - Kaynağa bağlı cevap üretimi

## F7-01 - Intent'e özel prompt mimarisini kur

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F6-04
- Tahmin: 1 gün

Yapılacaklar:

- Ortak güvenlik kuralları merkezi tutulur.
- Reference, definition, comparison, topic, scenario ve follow-up promptları ayrılır.
- Prompt sürümleri kaydedilir.

Zorunlu testler:

- Prompt snapshot ve gerekli alan testi.
- Kullanıcı metninin sistem kuralını değiştirememesi.

Tamamlanma kriteri:

- Her cevap hangi prompt sürümüyle üretildiği izlenebilir.

## F7-02 - Yapılandırılmış LLM çıktısı ve doğrulama ekle

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F7-01
- Tahmin: 1 gün

Yapılacaklar:

- Answer, details, citations ve limitations şeması tanımlanır.
- Geçersiz model çıktısı kontrollü ele alınır.

Zorunlu testler:

- Eksik alan, bozuk JSON, boş cevap ve fazla alan senaryoları.

Tamamlanma kriteri:

- Frontend yalnızca backend tarafından doğrulanmış cevap alır.

## F7-03 - Atıf doğrulama katmanı ekle

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F7-02
- Tahmin: 1 gün

Yapılacaklar:

- Modelin yazdığı her madde retrieval kaynaklarında aranır.
- Kaynaksız madde/iddia cevapta yayınlanmaz.

Zorunlu testler:

- Uydurma madde, yanlış madde ve doğru çoklu atıf.
- Kaynak sürümü eşleşmesi.

Tamamlanma kriteri:

- Kaynak dışı madde numarası üretim çıktısında %0.

## F7-04 - Gemini hata, timeout ve retry politikasını düzelt

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F7-02
- Tahmin: 0.5 gün

Yapılacaklar:

- `LLM hata verdi` başarılı cevap sayılmaz.
- Timeout, rate limit ve servis hatası ayrılır.
- Sınırlı retry ve güvenli fallback uygulanır.

Zorunlu testler:

- Mock timeout, 429, 5xx, boş ve kısa cevap.

Tamamlanma kriteri:

- Teknik LLM hata metni kullanıcıya hukuki cevap olarak dönmez.

## F7-05 - Cevap biçimi modlarını uygula

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F7-03
- Tahmin: 0.5 gün

Yapılacaklar:

- Kısa, detaylı ve otomatik modlar API sözleşmesine eklenir.
- Otomatik mod intent'e göre biçim seçer.

Zorunlu testler:

- Aynı soru için üç modun içerik tutarlılığı ve uzunluk sınırı.

Tamamlanma kriteri:

- Biçim değişirken kullanılan kaynak ve hukuki sonuç değişmez.

## F7-06 - Faithfulness evaluation oluştur

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F7-05
- Tahmin: 1 gün

Yapılacaklar:

- İddia-kaynak desteği, atıf doğruluğu, eksiklik ve kaynak dışı bilgi ölçülür.
- Otomatik metrikler kontrollü insan değerlendirmesiyle doğrulanır.

Zorunlu testler:

- Bilerek destekli, desteksiz ve kısmen destekli cevap fixture'ları.

Tamamlanma kriteri:

- Beta öncesi faithfulness en az %95 ve atıf doğruluğu en az %98.

### Faz 7 kalite kapısı

- Kaynak dışı madde numarası %0.
- Faithfulness en az %95.
- Atıf doğruluğu en az %98.
- LLM hata durumları güvenli.

# FAZ 8 - Konuşma hafızası

## F8-01 - Yapılandırılmış conversation state tasarla

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F4-04, F7-05
- Tahmin: 0.5 gün

Yapılacaklar:

- Aktif konu, son intent, hedefler, maddeler ve cevap modu tutulur.
- Ham geçmişin tamamını gönderme zorunluluğu kaldırılır.

Zorunlu testler:

- State şeması ve maksimum boyut.

Tamamlanma kriteri:

- Takip sorusu çözümlemesi için açık ve sınırlı state sözleşmesi vardır.

## F8-02 - Follow-up resolution geliştir

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F8-01
- Tahmin: 1 gün

Yapılacaklar:

- `bunun farkı ne`, `örnek ver`, `kısalt` gibi eksiltili sorular çözülür.
- Konu değişimi algılanır.

Zorunlu testler:

- Çok turlu konuşma seti, konu değişimi ve önceki konuya dönüş.

Tamamlanma kriteri:

- Takip sorusu çözümleme başarısı en az %90.

## F8-03 - Oturum izolasyonu ve süre sonunu uygula

- Durum: `BEKLIYOR`
- Sorumlu: `ORTAK`
- Bağımlılık: F8-02
- Tahmin: 0.5 gün

Yapılacaklar:

- Kullanıcılar arası state izolasyonu ve TTL uygulanır.
- Yeni sohbet temiz state ile başlar.

Zorunlu testler:

- İki eşzamanlı kullanıcı, süresi dolmuş oturum ve yeniden başlatma.

Tamamlanma kriteri:

- Bir kullanıcının konuşma bilgisi başka kullanıcıya sızamaz.

### Faz 8 kalite kapısı

- Çok turlu başarı en az %90.
- Oturum izolasyonu testleri başarılı.
- Token/context üst sınırı uygulanıyor.

# FAZ 9 - Ürün API'si, hesap ve güvenlik

## F9-01 - Sürümlü chatbot API sözleşmesini oluştur

- Durum: `BEKLIYOR`
- Sorumlu: `ORTAK`
- Bağımlılık: F7-05, F8-03
- Tahmin: 0.5 gün

Yapılacaklar:

- `/api/v1` session/message/feedback endpoint'leri tanımlanır.
- Request/response ve hata şemaları belgelenir.

Zorunlu testler:

- OpenAPI schema ve contract testleri.

Tamamlanma kriteri:

- Frontend ve backend aynı sürümlü sözleşmeyi kullanır.

## F9-02 - E-posta hesap ve oturum sistemini kur

- Durum: `BEKLIYOR`
- Sorumlu: `PLATFORM`
- Bağımlılık: F2-02
- Tahmin: 2 gün

Yapılacaklar:

- Kayıt, giriş, doğrulama, parola hash'i, sıfırlama ve token süresi uygulanır.

Zorunlu testler:

- Başarılı/başarısız giriş, brute force, süresi dolmuş token ve parola sıfırlama.

Tamamlanma kriteri:

- Düz metin parola tutulmaz; yetkisiz kullanıcı korunan veriye erişemez.

## F9-03 - Yetkilendirme ve veri izolasyonu ekle

- Durum: `BEKLIYOR`
- Sorumlu: `PLATFORM`
- Bağımlılık: F9-01, F9-02
- Tahmin: 1 gün

Yapılacaklar:

- Kullanıcı ve admin rolleri ayrılır.
- Session/message sahiplik kontrolleri uygulanır.

Zorunlu testler:

- Başkasının oturumuna erişme ve admin endpoint yetkisi.

Tamamlanma kriteri:

- ID değiştirilerek başka kullanıcı verisine erişilemez.

## F9-04 - API kötüye kullanım korumalarını ekle

- Durum: `BEKLIYOR`
- Sorumlu: `PLATFORM`
- Bağımlılık: F9-03
- Tahmin: 0.5 gün

Yapılacaklar:

- Rate limit, request boyutu, soru uzunluğu, CORS ve güvenlik header'ları.

Zorunlu testler:

- Rate limit, büyük istek, zararlı JSON, XSS metni ve SQL injection denemeleri.

Tamamlanma kriteri:

- Belgelenmiş limitler API tarafından uygulanır.

## F9-05 - Liveness ve readiness kontrollerini geliştir

- Durum: `BEKLIYOR`
- Sorumlu: `PLATFORM`
- Bağımlılık: F9-01
- Tahmin: 0.5 gün

Yapılacaklar:

- Process liveness ile DB/model readiness ayrılır.

Zorunlu testler:

- DB kapalı, model yüklenmemiş ve sağlıklı sistem senaryoları.

Tamamlanma kriteri:

- Trafik yalnızca hazır instance'a yönlendirilir.

### Faz 9 kalite kapısı

- Auth ve yetkilendirme testleri başarılı.
- Veri izolasyonu doğrulandı.
- Rate limit ve güvenlik sınırları aktif.
- API sözleşmesi sürümlü.

# FAZ 10 - Geri bildirim ve yönetici paneli

## F10-01 - Yapılandırılmış feedback veri modelini uygula

- Durum: `BEKLIYOR`
- Sorumlu: `PLATFORM`
- Bağımlılık: F9-03
- Tahmin: 0.5 gün

Yapılacaklar:

- Faydalı/faydasız, hata türü, açıklama ve inceleme durumu kaydedilir.

Zorunlu testler:

- Tekrar gönderim, sahiplik, silinen mesaj ve geçersiz hata türü.

Tamamlanma kriteri:

- Feedback mesaj, cevap sürümü ve kaynak setiyle ilişkilidir.

## F10-02 - Feedback inceleme akışını kur

- Durum: `BEKLIYOR`
- Sorumlu: `ORTAK`
- Bağımlılık: F10-01
- Tahmin: 0.5 gün

Yapılacaklar:

- `new`, `under_review`, `confirmed_issue`, `not_an_issue`,
  `added_to_evaluation`, `resolved` durumları uygulanır.

Zorunlu testler:

- Geçersiz durum geçişleri ve evaluation adayına dönüştürme.

Tamamlanma kriteri:

- Feedback otomatik üretim kuralına dönüşmez.

## F10-03 - Yönetici panelinin sistem görünümünü oluştur

- Durum: `BEKLIYOR`
- Sorumlu: `PLATFORM`
- Bağımlılık: F3-04, F9-05, F10-02
- Tahmin: 2 gün

Yapılacaklar:

- TCK sürümü, update adayı, ingest, sağlık, hata, latency ve maliyet görünümü.

Zorunlu testler:

- Admin yetkisi, boş veri, API hatası ve büyük liste.

Tamamlanma kriteri:

- Operasyonel kritik durumlar DB'ye doğrudan bağlanmadan görülebilir.

## F10-04 - RAG kalite görünümünü ekle

- Durum: `BEKLIYOR`
- Sorumlu: `ORTAK`
- Bağımlılık: F1-05, F10-03
- Tahmin: 1 gün

Yapılacaklar:

- Cevapsız sorular, hata türleri, yanlış madde raporları ve evaluation trendi.

Zorunlu testler:

- Metrik hesapları ile ham kayıt örneklerinin tutarlılığı.

Tamamlanma kriteri:

- RAG regressions yalnızca kullanıcı şikâyetine bağlı kalmadan görülebilir.

# FAZ 11 - Gizlilik ve veri yaşam döngüsü

## F11-01 - Veri envanteri ve saklama politikasını kararlaştır

- Durum: `BEKLIYOR`
- Sorumlu: `ORTAK`
- Bağımlılık: F9-03, F10-01
- Tahmin: 0.5 gün

Yapılacaklar:

- Hangi verinin neden, nerede ve ne kadar tutulduğu belgelenir.
- Konuşma kalite kullanımı için açık onay tanımlanır.

Zorunlu testler:

- Onaysız kullanıcının konuşmasının kalite veri setine girmemesi.

Tamamlanma kriteri:

- Her kişisel veri alanının amacı ve silme yolu tanımlıdır.

## F11-02 - Kişisel veri maskeleme hattını kur

- Durum: `BEKLIYOR`
- Sorumlu: `PLATFORM`
- Bağımlılık: F11-01
- Tahmin: 1 gün

Yapılacaklar:

- E-posta, telefon ve kimlik benzeri değerler kalite verisinden maskelenir.

Zorunlu testler:

- Türkçe veri biçimleri, yanlış pozitif ve kaçırma fixture'ları.

Tamamlanma kriteri:

- Ham kimlik bilgisi analitik/evaluation kopyasına taşınmaz.

## F11-03 - Kullanıcı veri silme sürecini uygula

- Durum: `BEKLIYOR`
- Sorumlu: `PLATFORM`
- Bağımlılık: F11-01
- Tahmin: 1 gün

Yapılacaklar:

- Hesap, oturum, mesaj, feedback ve ilişkili veriler için silme süreci.
- Yedeklerdeki davranış belgelenir.

Zorunlu testler:

- Tam silme, idempotent tekrar ve audit kaydı.

Tamamlanma kriteri:

- Kullanıcının erişilebilir üretim verisi doğrulanabilir biçimde silinir.

## F11-04 - Log redaction uygula

- Durum: `BEKLIYOR`
- Sorumlu: `PLATFORM`
- Bağımlılık: F11-02
- Tahmin: 0.5 gün

Yapılacaklar:

- Secret, token, parola ve ham konuşma içeriği loglardan çıkarılır.

Zorunlu testler:

- Hassas fixture'ların log snapshot'ında görünmemesi.

Tamamlanma kriteri:

- Üretim logları hassas kullanıcı veya secret verisi taşımaz.

# FAZ 12 - Gözlemlenebilirlik, performans ve maliyet

## F12-01 - Yapılandırılmış logging ve request tracing ekle

- Durum: `BEKLIYOR`
- Sorumlu: `PLATFORM`
- Bağımlılık: F11-04
- Tahmin: 0.5 gün

Yapılacaklar:

- Request ID, session ID, intent, model/prompt/index sürümü ve süreler kaydedilir.

Zorunlu testler:

- Bir isteğin backend-retrieval-LLM hattında izlenebilmesi.

Tamamlanma kriteri:

- Kullanıcı hatası hassas içerik açmadan teknik olarak incelenebilir.

## F12-02 - RAG latency ayrıştırmasını ekle

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`
- Bağımlılık: F12-01
- Tahmin: 0.5 gün

Yapılacaklar:

- Intent, embedding, DB, reranker, prompt ve LLM süreleri ayrı ölçülür.

Zorunlu testler:

- Toplam sürenin alt adımlarla tutarlı olması.

Tamamlanma kriteri:

- Yavaşlığın hangi katmandan geldiği ölçülebilir.

## F12-03 - DB pool ve model yaşam döngüsünü optimize et

- Durum: `BEKLIYOR`
- Sorumlu: `ORTAK`
- Bağımlılık: F12-02
- Tahmin: 1 gün

Yapılacaklar:

- Connection pool, tek model yükleme, warmup ve uygun pgvector index'i.

Zorunlu testler:

- Soğuk/sıcak başlangıç, pool tükenmesi ve model yükleme sayısı.

Tamamlanma kriteri:

- Her istek yeni model veya kontrolsüz DB bağlantısı oluşturmaz.

## F12-04 - Load ve soak testlerini çalıştır

- Durum: `BEKLIYOR`
- Sorumlu: `ORTAK`
- Bağımlılık: F12-03
- Tahmin: 1 gün

Yapılacaklar:

- 1, 5 ve 20 eşzamanlı kullanıcı; 24 saat düşük yük dayanıklılığı.

Zorunlu testler:

- P50/P95, hata oranı, bellek, DB pool ve rate limit davranışı.

Tamamlanma kriteri:

- Beta yükünde çoğu cevap 5-8 saniye hedefini karşılar veya sapma belgelenip
  yayın kararıyla kabul edilir.

## F12-05 - Soru ve kullanıcı başı maliyeti ölç

- Durum: `BEKLIYOR`
- Sorumlu: `ORTAK`
- Bağımlılık: F12-04
- Tahmin: 0.5 gün

Yapılacaklar:

- LLM token, altyapı ve depolama maliyeti senaryoları çıkarılır.

Zorunlu testler:

- Ölçülen kullanım ile fatura tahmininin örnek doğrulaması.

Tamamlanma kriteri:

- 20, 100 ve 1000 kullanıcı için aylık tahmin ve kullanım limiti kararı vardır.

# FAZ 13 - Deployment, yedekleme ve yayın güvenliği

## F13-01 - Beta altyapısını seç ve karar kaydı oluştur

- Durum: `BEKLIYOR`
- Sorumlu: `ORTAK`
- Bağımlılık: F12-05
- Tahmin: 0.5 gün

Yapılacaklar:

- Yönetilen servis/VPS seçenekleri maliyet, bakım ve taşınabilirlikle karşılaştırılır.

Zorunlu testler:

- Seçilen ortamın pgvector, secret, backup ve monitoring gereksinimini karşılaması.

Tamamlanma kriteri:

- Sağlayıcı kararı `DECISIONS.md` içinde gerekçelidir.

## F13-02 - Container ve production config oluştur

- Durum: `BEKLIYOR`
- Sorumlu: `PLATFORM`
- Bağımlılık: F13-01
- Tahmin: 1 gün

Yapılacaklar:

- Backend/frontend container, environment ayrımı ve secret injection.

Zorunlu testler:

- Temiz image build, non-root çalışma ve health check.

Tamamlanma kriteri:

- Yerel dosya veya geliştirici bilgisayarına bağlı olmayan üretim build'i vardır.

## F13-03 - Staging ortamını yayınla

- Durum: `BEKLIYOR`
- Sorumlu: `PLATFORM`
- Bağımlılık: F13-02
- Tahmin: 0.5 gün

Yapılacaklar:

- Production benzeri staging ve otomatik migration.

Zorunlu testler:

- Smoke, auth, chatbot, feedback ve admin E2E testleri.

Tamamlanma kriteri:

- Beta öncesi bütün yayın denemeleri staging'de yapılır.

## F13-04 - Backup ve restore sürecini doğrula

- Durum: `BEKLIYOR`
- Sorumlu: `PLATFORM`
- Bağımlılık: F13-03
- Tahmin: 0.5 gün

Yapılacaklar:

- Otomatik DB yedeği, saklama ve geri yükleme runbook'u.

Zorunlu testler:

- Gerçek staging yedeğinden boş DB'ye restore.
- Kayıt, sürüm ve kullanıcı bütünlüğü kontrolü.

Tamamlanma kriteri:

- Yedek yalnızca alınmış değil, geri yüklenerek doğrulanmıştır.

## F13-05 - Rollback ve incident runbook hazırla

- Durum: `BEKLIYOR`
- Sorumlu: `ORTAK`
- Bağımlılık: F13-04
- Tahmin: 0.5 gün

Yapılacaklar:

- Uygulama, migration, TCK sürümü ve model/prompt rollback adımları.

Zorunlu testler:

- Staging'de bir önceki stabil sürüme dönüş tatbikatı.

Tamamlanma kriteri:

- Kritik arızada izlenecek adımlar ve sorumlular bellidir.

# FAZ 14 - Beta öncesi kalite ve güvenlik kabulü

## F14-01 - Tam otomatik regression paketini çalıştır

- Durum: `BEKLIYOR`
- Sorumlu: `ORTAK`
- Bağımlılık: Faz 0-13 kalite kapıları
- Tahmin: 0.5 gün

Zorunlu testler:

- Unit, integration, retrieval, generation, E2E, security, migration ve frontend.

Tamamlanma kriteri:

- Kritik test başarısızlığı yoktur; kabul edilen istisnalar yazılıdır.

## F14-02 - Prompt injection ve güvenlik değerlendirmesi yap

- Durum: `BEKLIYOR`
- Sorumlu: `ORTAK`
- Bağımlılık: F14-01
- Tahmin: 0.5 gün

Zorunlu testler:

- Kuralları unutma, kaynak dışı cevap isteği, secret isteme, XSS/SQL ve yetki testleri.

Tamamlanma kriteri:

- Kritik/yüksek güvenlik açığı 0.

## F14-03 - Hukuk uzmanı örnek cevap incelemesini tamamla

- Durum: `BEKLIYOR`
- Sorumlu: `HUKUK`, `RAG`
- Bağımlılık: F14-01
- Tahmin: Harici

Yapılacaklar:

- Soru türü ve risk bazında örneklem cevaplar incelenir.
- Hatalar regression vakasına dönüştürülür.

Tamamlanma kriteri:

- Kritik hukuki hata çözümlenmiş veya beta engeli olarak kaydedilmiştir.

## F14-04 - Beta yayın kararı ver

- Durum: `BEKLIYOR`
- Sorumlu: `ORTAK`
- Bağımlılık: F14-02, F14-03
- Tahmin: 0.25 gün

Beta zorunlu eşikleri:

- Genel retrieval en az %90.
- Intent en az %95.
- Reference lookup yaklaşık %100.
- Atıf doğruluğu en az %98.
- Kaynak dışı madde numarası %0.
- Faithfulness en az %95.
- Kritik güvenlik açığı 0.
- Backup/restore ve rollback başarılı.

Tamamlanma kriteri:

- Go/no-go kararı metriklerle `DECISIONS.md` içine kaydedilmiştir.

# FAZ 15 - Kapalı beta ve piyasaya açılma

## F15-01 - 20-100 kullanıcıyla kapalı betayı başlat

- Durum: `BEKLIYOR`
- Sorumlu: `ORTAK`
- Bağımlılık: F14-04 GO kararı
- Tahmin: En az 2 hafta

Yapılacaklar:

- Kullanıcı bilgilendirmesi, destek kanalı ve feedback akışı açılır.
- Günlük sağlık, hata ve maliyet kontrolü yapılır.

Tamamlanma kriteri:

- Onaylı kullanıcı grubu ürüne erişir; izleme, destek ve geri bildirim kanalları
  gerçek kullanım altında çalışır.

## F15-02 - Beta hatalarını genel çözüm döngüsüyle işle

- Durum: `BEKLIYOR`
- Sorumlu: `RAG`, `PLATFORM`
- Bağımlılık: F15-01

Her doğrulanmış hata için:

1. Yeniden üretim.
2. Kök neden.
3. Regression testi.
4. Genel çözüm.
5. Tam evaluation.
6. Staging doğrulaması.
7. Kontrollü yayın.

Tamamlanma kriteri:

- Doğrulanmış kritik beta hatalarının regression testi ve çözüm/engel kaydı vardır;
  soruya özel geçici üretim kuralı eklenmemiştir.

## F15-03 - Beta sonuç raporunu oluştur

- Durum: `BEKLIYOR`
- Sorumlu: `ORTAK`
- Bağımlılık: F15-01

Rapor:

- Kullanıcı ve soru sayısı.
- Faydalı/faydasız oranı.
- Yanlış madde ve kaynak dışı cevap oranı.
- Answer/no-answer hataları.
- P50/P95 süre ve hata oranı.
- Kullanıcı/soru başı maliyet.
- En sık başarısız intent ve soru türleri.

Tamamlanma kriteri:

- Yayın kararında kullanılacak kalite, güvenlik, performans, maliyet ve kullanıcı
  geri bildirimi verileri tek sürümlü raporda toplanmıştır.

## F15-04 - Herkese açık yayın kalite kapısını değerlendir

- Durum: `BEKLIYOR`
- Sorumlu: `ORTAK`, `HUKUK`
- Bağımlılık: F15-02, F15-03

Zorunlu koşullar:

- Genel retrieval en az %95.
- Kritik alt gruplarda kabul edilebilir ayrı sonuçlar.
- Kaynak dışı madde numarası %0.
- Atıf ve faithfulness hedefleri korunuyor.
- TCK update/rollback, backup/restore ve veri silme çalışıyor.
- Gerçek maliyet ve kapasite kabul edilmiş.
- Açık kritik/yüksek güvenlik veya hukuki hata yok.

Tamamlanma kriteri:

- Piyasa yayını için gerekçeli GO kararı vardır.

# Önerilen 8 haftalık paralel takvim

| Hafta | RAG sorumlusu | Platform sorumlusu | Ortak kapı |
|---|---|---|---|
| 1 | F1 test ve baseline | F0 temizlik/CI | Faz 0-1 |
| 2 | F3 parser/ingest | F2 migration | Faz 2-3 |
| 3 | F4 Intent Engine 2.0 | F9 auth başlangıcı | Faz 4 |
| 4 | F5 intent-aware retrieval | F9 API/auth | Faz 5 |
| 5 | F6 scoring/reranker | F10 feedback | Faz 6 |
| 6 | F7 cevap/atıf | F10 admin | Faz 7 |
| 7 | F8 hafıza, evaluation | F11-13 deployment/izleme | Faz 8-13 |
| 8 | Performans ve güvenlik | Load/backup/staging | Faz 14 |

Bu tablo yön gösterir; görev bağımlılıkları ve kalite kapıları takvimden önce gelir.

# İlk yürütme sırası

Proje takip belgeleri tamamlandıktan sonra ilk kod çalışma sırası:

1. F0-01 - Secret rotasyonu.
2. F0-02 - Depo temizliği.
3. F0-03/F0-04 - Temiz kurulum.
4. F0-05 - CI.
5. F1-01 - Intent runner düzeltmesi.
6. F1-02 - Pytest dönüşümü.
7. F1-03/F1-04 - Evaluation şeması ve metrik motoru.
8. F1-05 - Kanonik baseline.
9. F2/F3 - Veri ve ingest temeli.
10. F4-02 - Multi-definition düzeltmesi.
11. F5-01 - Reference retrieval.
12. F6-01 - Reranker entegrasyonu.

# Plan değişikliği kuralı

- Görev silme, kalite eşiği düşürme, faz sırası değiştirme veya kapsam genişletme
  kararı `DECISIONS.md` içine gerekçesiyle yazılır.
- Bir görev tahmin edilenden uzun sürerse test veya güvenlik kısmı çıkarılmaz;
  kapsam ya da takvim yeniden planlanır.
- Her oturum sonunda aktif görev ve sıradaki adım `CURRENT_STATUS.md` ile
  `SESSION_LOG.md` içine kaydedilir.
