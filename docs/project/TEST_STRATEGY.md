# HMGS Chatbot - Test Stratejisi

## 1. Amaç

Bu belge, HMGS TCK chatbotunda bir özelliğin veya düzeltmenin nasıl doğrulanacağını
tanımlar. Testlerin amacı yalnızca kodun çalıştığını göstermek değil; doğru hukuki
kaynağın bulunduğunu, cevabın kaynağa bağlı kaldığını, sistemin gerektiğinde cevap
vermediğini, kullanıcı verisinin korunduğunu ve önceki davranışların bozulmadığını
kanıtlamaktır.

## 2. Değişmez test ilkeleri

1. Testi olmayan görev tamamlanmış sayılmaz.
2. Hata düzeltilmeden önce mümkünse hatayı yeniden üreten test yazılır.
3. Göreve özel testten sonra tam regression paketi çalışır.
4. Test sorusuna özel keyword eklemek kabul edilmez.
5. Tuning/development seti ile final holdout seti ayrılır.
6. Başarısız vaka silinmez; beklenti değişiyorsa karar kaydı gerekir.
7. Retrieval ve LLM cevabı ayrı değerlendirilir.
8. Genel accuracy alt grup başarısızlığını gizleyemez.
9. Rastlantısal LLM testlerinde model, prompt, sıcaklık ve tarih kaydedilir.
10. Her sonuç kod commit'i, DB sürümü, embedding indeksi ve prompt sürümüyle bağlanır.

## 3. Test piramidi

```text
                    Manuel hukuk incelemesi
                  Güvenlik / red-team testleri
                Uçtan uca chatbot senaryoları
             Generation ve faithfulness testleri
           Retrieval/reranking integration testleri
        Intent, parser, scoring ve policy unit testleri
```

Alt katmanlar hızlı ve deterministik; üst katmanlar daha az sayıda fakat ürün
davranışını doğrulayan testlerdir.

## 4. Test dizin hedefi

```text
tests/
├── unit/
│   ├── intent/
│   ├── parser/
│   ├── scoring/
│   ├── policies/
│   └── citations/
├── integration/
│   ├── database/
│   ├── ingestion/
│   ├── retrieval/
│   ├── reranking/
│   └── generation/
├── e2e/
│   ├── chat/
│   ├── follow_up/
│   └── feedback/
├── security/
├── performance/
├── fixtures/
└── evaluation/
```

## 5. Test katmanları

### 5.1. Statik ve kurulum kontrolleri

- Python compile/import kontrolü.
- Python lint ve type kontrolü.
- Frontend lint ve production build.
- Secret scan.
- Bağımlılık güvenlik taraması.
- Temiz virtualenv ve `npm ci` kurulumu.

Her pull request'te çalışır.

### 5.2. Parser testleri

Doğrulanacak yapılar:

- Normal madde,
- Çok fıkralı madde,
- Bent ve alt bent,
- Ek/geçici/mülga madde,
- Değişiklik notları,
- Sayfa başlığı ve dipnot,
- Satır sonunda bölünmüş kelime,
- Boş/bozuk sayfa.

Metrikler:

- Madde numarası exact match,
- Başlık exact/normalize match,
- Metin kaybı oranı,
- Tekrarlanan metin oranı,
- Deterministik chunk hash eşleşmesi.

Çıkış kriteri: Kaynak metnin hukuki anlam taşıyan bölümleri kaybolmamalı; aynı girdi
aynı parser/chunking sürümünde aynı sonucu üretmelidir.

### 5.3. Intent testleri

Her vaka şu alanları taşımalıdır:

```json
{
  "id": "intent_comparison_001",
  "question": "Hırsızlık ile yağma arasındaki fark nedir?",
  "expected_intent": "comparison",
  "expected_relation": "comparison",
  "expected_targets": ["hırsızlık", "yağma"],
  "expected_articles": []
}
```

Ayrı ölçümler:

- Intent accuracy,
- Relation accuracy,
- Target count accuracy,
- Target exact match,
- Article extraction accuracy,
- Clarification karar doğruluğu,
- Follow-up resolution doğruluğu.

Alt gruplar:

- Reference,
- Single concept,
- Multi-definition,
- Comparison,
- Topic explanation,
- Scenario,
- Follow-up,
- Unsupported legal,
- Out-of-scope,
- Ambiguous.

Beta hedefleri:

- Genel intent: en az %95,
- Reference article extraction: en az %99,
- Comparison target exact match: en az %95,
- Follow-up resolution: en az %90.

### 5.4. Retrieval testleri

Kanonik vaka şeması:

```json
{
  "id": "retrieval_comparison_001",
  "question": "Hırsızlık ile yağma arasındaki fark nedir?",
  "question_type": "comparison",
  "required_articles": ["141", "148"],
  "acceptable_articles": [],
  "forbidden_articles": [],
  "should_answer": true
}
```

Metrikler:

- Recall@1, Recall@3, Recall@5,
- Precision@K,
- MRR,
- NDCG,
- Required article coverage,
- Forbidden article hit rate,
- Empty result rate.

Soru türü bazında rapor zorunludur. Genel retrieval sonucu tek başına yayın kapısını
geçiremez.

Beta hedefleri:

- Genel retrieval: en az %90,
- Reference lookup: yaklaşık %100,
- Kritik soru türlerinin her biri: en az %90 Recall@5,
- Herkese açık yayın genel hedefi: en az %95.

### 5.5. Scoring ve reranker testleri

- Her skor bileşeni için unit test.
- Aynı sinyalin çift ödüllendirilmesi kontrolü.
- Reranker çıktısının gerçekten son sıralamayı belirlediği test.
- Reranker açık/kapalı A/B evaluation.
- Ablation: Her sinyal kaldırıldığında kalite etkisi.
- P50/P95 gecikme ve bellek etkisi.

Reranker yalnızca kalite faydası gecikme ve kaynak maliyetini haklı çıkarıyorsa aktif
kalır.

### 5.6. Answer/no-answer policy testleri

Confusion matrix:

| Beklenen / Gerçek | Answer | No-answer |
|---|---:|---:|
| Answer | Doğru cevap kararı | Gereksiz ret |
| No-answer | Riskli yanlış cevap | Doğru ret |

Özellikle ölçülecekler:

- TCK'da destek olmayan teori,
- TCK dışı hukuk sorusu,
- Kapsam dışı soru,
- Eksik/belirsiz senaryo,
- Kişisel hukuki danışmanlık isteği,
- Retrieval zayıf veya çelişkili durum.

Hukuki risk nedeniyle yanlış cevap verme oranı, gereksiz ret oranından daha yüksek
önceliklidir; ancak ürünün sürekli cevap vermemesi de ayrı regression kabul edilir.

### 5.7. Generation ve faithfulness testleri

Her cevap şu açılardan değerlendirilir:

- TCK bağlamına bağlılık,
- Desteksiz iddia,
- Madde numarası doğruluğu,
- Atıf-iddia uyumu,
- Gerekli bilginin eksik bırakılması,
- Soruya doğrudan cevap,
- Kısa/detaylı biçim uyumu,
- Hukuki danışmanlık sınırı.

Yapılandırılmış çıktı testleri:

- Bozuk JSON,
- Eksik alan,
- Uydurma citation,
- Retrieval'da olmayan madde,
- Boş/kısa cevap,
- Gemini timeout, 429 ve 5xx.

Beta hedefleri:

- Faithfulness: en az %95,
- Atıf doğruluğu: en az %98,
- Retrieval dışında madde numarası: %0.

### 5.8. Çok turlu konuşma testleri

Örnek akışlar:

```text
Olası kast nedir?
Bilinçli taksirden farkı ne?
Bir örnek ver.
Daha kısa anlat.
```

Doğrulanacaklar:

- Aktif konu,
- Eksik hedefin önceki turdan çözülmesi,
- Konu değişimi,
- Yeni oturumda temiz state,
- Kullanıcılar arası izolasyon,
- Token/context sınırı,
- Oturum süresi sonu.

### 5.9. API ve güvenlik testleri

- Auth ve token süresi,
- Başkasının session/message verisine erişme,
- Admin rolü,
- Rate limit,
- Büyük/bozuk request,
- SQL injection ve XSS metni,
- Prompt injection,
- Secret isteme,
- CORS ve güvenlik header'ları,
- Log redaction,
- Kullanıcı veri silme.

Beta kapısı: Kritik/yüksek açık 0.

### 5.10. Migration, backup ve restore testleri

- Boş DB upgrade,
- Eski şemadan upgrade,
- Downgrade/re-upgrade,
- Yarıda kalan migration,
- Aynı migration'ın tekrar uygulanması,
- Staging yedeğinden boş DB'ye restore,
- TCK ve uygulama rollback.

Yedek yalnızca oluşturulmuşsa değil, geri yüklenmişse başarılı sayılır.

### 5.11. Performans testleri

Senaryolar:

- Tek kullanıcı,
- 5 eşzamanlı kullanıcı,
- 20 eşzamanlı kullanıcı,
- Soğuk/sıcak başlangıç,
- Uzun soru ve uzun konuşma,
- 24 saat düşük yük soak testi,
- DB pool tükenmesi,
- LLM rate limit.

Metrikler:

- P50/P95/P99 latency,
- Hata oranı,
- CPU/bellek,
- DB bağlantısı,
- Token ve soru başı maliyet.

Beta hedefi: Çoğu cevap 5-8 saniye; sapmalar alt adım süreleriyle açıklanmalıdır.

## 6. Evaluation veri yönetimi

Veri bölümleri:

- `development`: Hata analizi ve geliştirme sırasında görülebilir.
- `regression`: Doğrulanmış geçmiş hatalar.
- `holdout`: Günlük tuning sırasında görülmez; faz/yayın kapısında çalışır.
- `beta_candidate`: Kullanıcı geri bildiriminden gelen, henüz doğrulanmamış vakalar.

Kurallar:

- Aynı normalize soru iki bölüme yanlışlıkla giremez.
- Beklenen sonuç değişikliği inceleme gerektirir.
- Kullanıcı konuşması kişisel veri temizlenmeden test setine eklenmez.
- Otomatik üretilen sorular uzman/manuel doğrulama olmadan holdout olamaz.

## 7. Her görevde çalıştırılacak minimum test

| Değişiklik | Zorunlu minimum |
|---|---|
| Intent | Intent unit + 300 regression + ilgili holdout |
| Parser/chunking | Parser fixture + ingest integration + retrieval smoke |
| Embedding/model | Tam yeniden indeks + retrieval evaluation |
| Scoring/reranker | Unit + ablation/A-B + tam retrieval |
| Prompt/model | Generation schema + citation + faithfulness |
| API/auth | Contract + security + E2E |
| DB migration | Upgrade/downgrade + veri bütünlüğü |
| Frontend | Lint + build + kritik kullanıcı akışı |
| Deployment | Staging smoke + health + rollback |

## 8. Sonuç kaydı

Her önemli koşu en az şu bilgileri taşır:

```text
run_id
timestamp
git_commit
branch
test_suite_version
database_version
source_document_version
embedding_model/index_version
reranker_version
prompt_version
llm_model
metrics
failed_case_ids
latency
estimated_cost
```

Özet `TEST_RESULTS.md` içinde; ayrıntılı makine çıktısı sürümlü evaluation artifact'i
olarak tutulur.

## 9. Regression kabul kuralı

Bir değişiklik genel metriği artırsa bile aşağıdaki durumlardan biri varsa otomatik
kabul edilmez:

- Reference lookup bozulduysa,
- Kaynak dışı madde oluştuysa,
- Kritik soru grubunda anlamlı düşüş varsa,
- False-answer oranı yükseldiyse,
- Kullanıcı izolasyonu/güvenlik bozulduysa,
- P95 veya maliyet kabul edilmemiş düzeyde arttıysa.

Kabul edilen her istisna `DECISIONS.md` içinde gerekçelendirilir.

## 10. Yayın kapıları

### Kapalı beta

- Genel retrieval >= %90,
- Intent >= %95,
- Reference extraction >= %99,
- Reference lookup yaklaşık %100,
- Atıf doğruluğu >= %98,
- Faithfulness >= %95,
- Kaynak dışı madde %0,
- Kritik/yüksek güvenlik açığı 0,
- Backup/restore ve rollback başarılı.

### Herkese açık yayın

- Genel retrieval >= %95,
- Kritik alt grupların ayrı eşikleri başarılı,
- Beta sırasında doğrulanmış kritik hata açık değil,
- Gerçek latency/maliyet kabul edilmiş,
- TCK güncelleme ve veri silme süreçleri test edilmiş,
- Hukuk uzmanı örneklem incelemesi tamamlanmış.

