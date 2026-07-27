# HMGS Chatbot - Ürün Kapsamı

## Belge bilgisi

- Belge durumu: Onaylı başlangıç kapsamı
- Ürün aşaması: Kapalı beta hazırlığı
- İlk hedef sürüm: HMGS Ceza Hukuku / TCK chatbotu
- Hedef beta kullanıcı sayısı: 20-100
- Hedef beta hazırlık süresi: 1-2 ay

Bu belge, ürünün ilk sürümde ne olduğunu ve ne olmadığını tanımlar. Teknik kararlar,
özellik talepleri ve geliştirme görevleri bu sınırlar dikkate alınarak değerlendirilir.
Kapsamı değiştiren bir karar alınırsa `DECISIONS.md` içinde gerekçeli bir karar kaydı
oluşturulmadan bu belge değiştirilmez.

## 1. Ürün vizyonu

HMGS Chatbot; Hukuk Mesleklerine Giriş Sınavı'na hazırlanan öğrencilerin Türk Ceza
Kanunu'nu güvenilir, kaynak gösteren ve anlaşılır cevaplarla çalışmasına yardımcı
olan web tabanlı bir eğitim asistanıdır.

Ürünün ilk sürümünün temel vaadi şudur:

> Kullanıcının Ceza Hukuku ve TCK kapsamındaki sorusunu doğru anlayarak yalnızca
> doğrulanmış güncel TCK içeriğine dayalı, açık madde atıfları içeren ve kaynakta
> desteklenmeyen bilgi üretmeyen cevap sunmak.

## 2. Hedef kullanıcı

İlk sürümün birincil hedef kullanıcısı:

- HMGS sınavına hazırlanan öğrenciler.

İlk sürüm aşağıdaki kullanıcı grupları için özel olarak tasarlanmaz:

- Kişisel hukuki danışmanlık arayan vatandaşlar,
- Müvekkil dosyası üzerinde çalışan avukatlar,
- Hâkim, savcı veya diğer hukuk profesyonellerinin mesleki karar süreçleri,
- Bütün hukuk fakültesi derslerini kapsayan genel amaçlı hukuk öğrencileri.

Bu kullanıcıların sisteme erişebilmesi, ürünün onlar için hukuki danışmanlık veya
mesleki karar desteği sunduğu anlamına gelmez.

## 3. İlk sürümün bilgi kapsamı

İlk sürümün tek hukuki bilgi kaynağı güncel Türk Ceza Kanunu'dur.

Kullanılan kaynak için aşağıdaki koşullar zorunludur:

- Kaynak resmî ve doğrulanabilir olmalıdır.
- Kaynak sürümü kayıt altına alınmalıdır.
- Her cevapta kullanılan madde veya maddeler izlenebilmelidir.
- Kanun değişikliği algılandığında yeni sürüm otomatik olarak yayına alınmamalıdır.
- Değişiklik yönetici tarafından incelenip onaylandıktan sonra indekslenmelidir.
- Başarısız güncellemede son doğrulanmış sürüme geri dönülebilmelidir.

İlk sürümün bilgi kapsamına dahil olmayan kaynaklar:

- Ceza Hukuku ders notları,
- Ders kitapları ve yayınevi içerikleri,
- Doktrin,
- Yargıtay veya diğer mahkeme kararları,
- İnternet makaleleri,
- Modelin genel hukuk bilgisi,
- TCK dışındaki kanun ve mevzuat.

## 4. Desteklenen soru türleri

Chatbot ilk sürümde aşağıdaki soru türlerini destekler:

1. Açık madde sorguları
   - Örnek: "TCK 141 ne diyor?"
2. Tek kavram veya suç tipi soruları
   - Örnek: "Hırsızlık suçu nedir?"
3. Kavram veya suç karşılaştırmaları
   - Örnek: "Hırsızlık ile yağma arasındaki fark nedir?"
4. TCK sınırları içinde konu anlatımı
   - Örnek: "TCK'ya göre kast ve taksiri anlat."
5. Kısa eğitim senaryoları
   - Kullanıcının verdiği olay, yalnızca TCK metninde açıkça desteklenebilen unsurlar
     üzerinden eğitim amacıyla değerlendirilir.
6. Sınav odaklı örnekler
   - Üretilen örnekler açıkça eğitim örneği olarak sunulur ve TCK dışı bilgi eklemez.
7. Aynı konuşma içindeki takip soruları
   - Örnek: "Bilinçli taksirden farkı ne?" veya "Bunu daha kısa anlat."

Her soru türü ortak RAG altyapısını kullanır; ancak intent tespiti, retrieval
stratejisi, bağlam oluşturma biçimi, cevap şablonu ve test seti ayrı olabilir.

## 5. Cevap biçimi

Kullanıcı aşağıdaki cevap biçimlerinden birini seçebilir:

- Kısa,
- Detaylı,
- Otomatik.

Otomatik modda sistem soru türüne uygun biçimi seçer. Genel kurallar:

- Açık madde sorusu doğrudan ve kısa cevaplanır.
- Karşılaştırma sorusu iki tarafı dengeli ve yapılandırılmış biçimde açıklar.
- Konu anlatımı anlaşılır başlıklarla sunulur.
- Senaryo cevabı olay unsurları, sınırlamalar ve ilgili maddeleri ayırır.
- Takip sorusu önceki cevabı gereksiz yere tekrar etmez.
- Her hukuki iddia ilgili TCK maddesiyle ilişkilendirilir.
- Kullanıcıya retrieval skoru veya sistem içi teknik hata metni gösterilmez.

## 6. Konuşma hafızası

İlk sürüm aynı sohbet oturumu içinde konuşma bağlamını korur.

- Önceki hedef kavramlar ve maddeler takip sorularında kullanılabilir.
- Bir kullanıcının bağlamı başka kullanıcıya aktarılamaz.
- Bütün sohbet geçmişi kontrolsüz biçimde modele gönderilmez.
- Oturum süresi ve bağlam boyutu sınırlıdır.
- Kalıcı kullanıcı sohbet geçmişi ilk sürümün zorunlu özelliği değildir.

## 7. Hukuki rol ve güvenlik sınırı

Ürün yalnızca eğitim ve sınava hazırlık amacı taşır.

Chatbot:

- Kişisel hukuki danışmanlık yapmaz.
- Kullanıcının gerçek uyuşmazlığı için kesin sonuç veya eylem talimatı vermez.
- Avukat, hâkim veya başka bir hukuk profesyonelinin yerine geçmez.
- TCK dışında kalan bilgiyle boşluk doldurmaz.
- Kaynakta açık destek bulunmadığında bunu dürüstçe belirtir.
- Belirsiz sorularda gerekli olduğunda açıklayıcı soru sorar.
- Modelin genel bilgisini hukuki kaynak gibi kullanmaz.

Kullanıcı arayüzünde ürünün eğitim amacı ve kapsam sınırı açıkça gösterilir.

## 8. İlk yayın modeli

İlk yayın herkese açık geniş lansman değil, kapalı beta olacaktır.

- Beta kullanıcı sayısı: 20-100 HMGS öğrencisi.
- Kullanıcılar basit e-posta ve parola hesabıyla giriş yapar.
- Kullanım, hata, maliyet ve performans ölçülür.
- Kullanıcılar cevaplara yapılandırılmış geri bildirim verebilir.
- Kritik kalite eşikleri sağlanmadan ürün herkese açılmaz.

## 9. Yönetim gereksinimleri

İlk sürüm temel bir yönetici paneli içerir. Panel en az aşağıdakileri gösterir:

- Aktif TCK sürümü,
- Son güncelleme kontrolü,
- Onay bekleyen mevzuat değişiklikleri,
- Belge işleme ve indeksleme durumu,
- Sistem sağlığı,
- Cevap süreleri ve hata oranları,
- Cevapsız sorular,
- Kullanıcı geri bildirimleri,
- Yanlış madde ve kaynak uyumsuzluğu bildirimleri,
- Kullanım ve tahmini maliyet.

## 10. Geri bildirim ve ürün geliştirme

Kullanıcılar aşağıdaki geri bildirimleri verebilir:

- Faydalı / faydasız,
- Yanlış madde,
- Cevap kaynakla uyuşmuyor,
- Soru yanlış anlaşıldı,
- Cevap eksik,
- Gereksiz yere cevap verilmedi,
- Kaynak gösterimi hatalı,
- Kısa açıklama.

Kullanıcı geri bildirimi otomatik olarak retrieval kuralı, prompt veya test beklentisi
haline gelmez. Önce yetkili kişi tarafından incelenir; doğrulanırsa regression testine
dönüştürülür ve genel çözüm geliştirilir.

## 11. Gizlilik ve veri saklama

- Konuşmalar kalite geliştirme amacıyla yalnızca açık bilgilendirme ve kullanıcı
  onayıyla sınırlı süre saklanabilir.
- Saklanan metinler kişisel bilgilerden arındırılmalıdır.
- Kullanıcı verisinin silinmesini talep edebilmelidir.
- E-posta ve kimlik bilgileri analitik verilerden ayrılmalıdır.
- Uygulama logları varsayılan olarak ham konuşma içeriği veya gizli bilgi taşımamalıdır.

Kesin saklama süresi ve ayrıntılı politika piyasaya açılmadan önce hukuk ve gizlilik
gereksinimleri dikkate alınarak ayrıca karara bağlanır.

## 12. Kalite hedefleri

### Kapalı beta öncesi

- Genel retrieval başarısı: en az %90,
- Intent doğruluğu: en az %95,
- Açık madde sorgularında hedef: yaklaşık %100,
- Atıf doğruluğu: en az %98,
- Kaynak dışı madde numarası üretme oranı: %0,
- Kaynağa bağlılık hedefi: en az %95,
- Kritik güvenlik açığı: 0,
- Çoğu cevap için hedef süre: 5-8 saniye.

### Herkese açık yayın öncesi

- Genel retrieval başarısı: en az %95,
- Kritik soru türlerinde ayrı kalite eşikleri sağlanmış olmalı,
- Kanun güncelleme ve geri dönüş süreci test edilmiş olmalı,
- Yedekleme ve geri yükleme doğrulanmış olmalı,
- Kullanıcı verisi silme süreci çalışmalı,
- Gerçek beta verileriyle maliyet ve kapasite ölçülmüş olmalı,
- Örnek cevaplar hukuk alanı uzmanı tarafından incelenmiş olmalı.

Bu oranların hesaplama yöntemi `TEST_STRATEGY.md` içinde tanımlanacaktır. Yalnızca
genel bir accuracy değeri kalite kapısını geçmek için yeterli değildir.

## 13. İlk sürüm dışında kalan özellikler

Aşağıdaki özellikler gelecekte değerlendirilebilir ancak ilk chatbot ürününün zorunlu
kapsamında değildir:

- Bütün HMGS dersleri,
- TCK dışındaki kanunlar,
- Doktrin ve yargı kararı retrieval'ı,
- Kalıcı sohbet geçmişi,
- Mobil uygulama,
- Sesli görüşme,
- Hukuki belge veya dava dosyası analizi,
- Kişiselleştirilmiş hukuki danışmanlık,
- Quiz, dashboard ve senaryo modüllerinin yeni özelliklerle genişletilmesi,
- Otomatik öğrenme veya kullanıcı geri bildiriminden otomatik kural üretme.

Mevcut quiz, dashboard ve senaryo kodları korunabilir; ancak chatbot kapalı beta kalite
kapısını geçene kadar bu modüllere yeni özellik eklenmesi ana geliştirme planının parçası
değildir.

## 14. Ekip ve sorumluluk sınırı

Ekip iki yazılım mühendisliği öğrencisinden oluşur.

- Chatbot/RAG sorumlusu: Intent Engine, retrieval, reranker, prompt, cevap güvenliği,
  evaluation ve RAG performansı.
- Platform sorumlusu: Hesap sistemi, yönetici paneli, deployment, kullanıcı geri
  bildirimi, izleme ve operasyon altyapısı.
- Ortak sorumluluk: API sözleşmeleri, veritabanı migration'ları, entegrasyon testleri,
  güvenlik ve yayın kararı.

Hukuki içerik doğrulaması için kapalı beta sürecinde hukuk alanından bir uzmanın örnek
cevapları incelemesi planlanır.

## 15. Kapsam değişikliği kuralı

Yeni bir özellik veya kaynak talebi geldiğinde aşağıdaki sorular cevaplanır:

1. İlk sürümün temel vaadine doğrudan katkı sağlıyor mu?
2. Mevcut kalite kapısını geciktiriyor mu?
3. Yeni hukuki veya gizlilik riski oluşturuyor mu?
4. Test edilebilir kabul kriteri var mı?
5. Mimariyi diğer hukuk alanlarına genişlemeyi zorlaştıracak biçimde TCK'ya kilitliyor mu?

Kapsamı değiştiren kararlar `DECISIONS.md` içinde kayıt altına alınmadan uygulamaya
alınmaz.
