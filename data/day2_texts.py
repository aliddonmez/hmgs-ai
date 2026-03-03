# data/day2_texts.py

TEXTS = [
    {
        "id": 1,
        "title": "Hırsızlık suçu tanım ve korunan yarar",
        "text": (
            "Hırsızlık, başkasına ait taşınır bir malın zilyedinin rızası olmadan alınmasıdır. "
            "Bu suçta korunan hukuki değer, mülkiyet ve zilyetlik ilişkisidir. "
            "Fail, malı kendi yararına veya başkasının yararına elde etmek amacıyla hareket eder."
        ),
        "expected_group": "theft",
    },
    {
        "id": 2,
        "title": "Hırsızlıkta maddi unsur ve hareket",
        "text": (
            "Hırsızlık suçunun maddi unsuru, taşınır mal üzerinde zilyetliğin fiilen el değiştirmesidir. "
            "Alma hareketi, malın bulunduğu yerden çıkarılmasıyla tamamlanabilir. "
            "Zilyedin rızası yoksa ve mal başkasına aitse, tipiklik yönünden temel şartlar oluşur."
        ),
        "expected_group": "theft",
    },
    {
        "id": 3,
        "title": "Hırsızlıkta kast ve suçun unsurları",
        "text": (
            "Hırsızlık kasten işlenebilir; failin malı bilerek ve isteyerek alması gerekir. "
            "Hata hâlinde kastın varlığı tartışılır. "
            "Suçun unsurları; başkasına ait taşınır mal, zilyedin rızasının bulunmaması ve alma hareketidir."
        ),
        "expected_group": "theft",
    },
    {
        "id": 4,
        "title": "Dolandırıcılık suçu tanım ve hile",
        "text": (
            "Dolandırıcılık, hileli davranışlarla bir kimsenin aldatılması ve bu aldanma sonucu "
            "kendisine veya başkasına yarar sağlanmasıdır. "
            "Hile ile mağdurun iradesi sakatlanır ve malvarlığı zarar görür."
        ),
        "expected_group": "fraud",
    },
    {
        "id": 5,
        "title": "Ceza hukukunda kast kavramı",
        "text": (
            "Kast, suçun kanuni tanımındaki unsurların bilerek ve istenerek gerçekleştirilmesidir. "
            "Doğrudan kast ve olası kast ayrımı, neticenin öngörülmesi ve kabullenilmesi üzerinden yapılır. "
            "Kastın varlığı olayın şartlarından çıkarılır."
        ),
        "expected_group": "mens_rea",
    },
    {
        "id": 6,
        "title": "Ceza hukukunda taksir kavramı",
        "text": (
            "Taksir, dikkat ve özen yükümlülüğüne aykırılık sonucu istenmeyen bir neticenin meydana gelmesidir. "
            "Bilinçli taksirde netice öngörülür fakat gerçekleşmeyeceği düşünülür. "
            "Taksirin varlığı, öngörülebilirlik ve tedbirsizlik kriterleriyle değerlendirilir."
        ),
        "expected_group": "mens_rea",
    },
    {
        "id": 7,
        "title": "Borçlar hukukunda sözleşmenin kurulması",
        "text": (
            "Sözleşme, tarafların karşılıklı ve birbirine uygun irade beyanlarıyla kurulur. "
            "Teklif ve kabul, esaslı noktalarda uyuşmayı sağlamalıdır. "
            "İrade sakatlıkları ve şekil şartları, sözleşmenin geçerliliğini etkileyebilir."
        ),
        "expected_group": "contract",
    },
    {
        "id": 8,
        "title": "Borçlar hukukunda haksız fiil sorumluluğu",
        "text": (
            "Haksız fiil sorumluluğu için hukuka aykırı fiil, zarar, kusur ve illiyet bağı gerekir. "
            "Tazminatın kapsamı zararın niteliğine göre belirlenir. "
            "Kusursuz sorumluluk halleri ayrıca düzenlenebilir."
        ),
        "expected_group": "tort",
    },
    {
        "id": 9,
        "title": "Futbolda ofsayt kuralı",
        "text": (
            "Ofsayt, hücum oyuncusunun top kendisine atıldığı anda rakip kale çizgisine "
            "top ve sondan ikinci savunmacıdan daha yakın olmasıyla ilgilidir. "
            "Oyuna aktif katılım şartı değerlendirmeyi değiştirir."
        ),
        "expected_group": "unrelated",
    },
    {
        "id": 10,
        "title": "Kahve demleme oranı",
        "text": (
            "Filtre kahvede yaygın oran, 1 gram kahveye 15-17 gram su olacak şekilde ayarlanır. "
            "Öğütüm kalınlığı ve su sıcaklığı tat profilini belirgin biçimde etkiler. "
            "Demleme süresi genelde 2.5-4 dakika aralığındadır."
        ),
        "expected_group": "unrelated",
    },
    {
        "id": "CH_006",
        "dersadi": "Ceza Hukuku",
        "konu": "Hırsızlık Suçu",
        "soru": "Hırsızlık suçunda korunan hukuki değer aşağıdakilerden hangisidir?",
        "secenekler": [
            "Kamu düzeni",
            "Mülkiyet ve zilyetlik ilişkisi",
            "Kişisel onur",
            "Devlet güvenliği",
            "Aile düzeni",
        ],
        "dogru_cevap": 1,
        "aciklama": "Hırsızlık suçunda korunan hukuki değer, mülkiyet ve zilyetlik ilişkisidir.",
        "kaynak": "TCK m.141",
        "zorluk": 2,
    },
    {
        "id": "CH_007",
        "dersadi": "Ceza Hukuku",
        "konu": "Hırsızlık Suçu",
        "soru": "Hırsızlık suçunda alma hareketi ne zaman tamamlanmış sayılır?",
        "secenekler": [
            "Failin malı görmesiyle",
            "Malın değerinin belirlenmesiyle",
            "Malın bulunduğu yerden çıkarılmasıyla",
            "Mağdurun şikâyetiyle",
            "Failin yakalanmasıyla",
        ],
        "dogru_cevap": 2,
        "aciklama": "Alma hareketi, malın bulunduğu yerden çıkarılmasıyla tamamlanabilir.",
        "kaynak": "TCK m.141",
        "zorluk": 2,
    },
    {
        "id": "CH_008",
        "dersadi": "Ceza Hukuku",
        "konu": "Hırsızlık Suçu",
        "soru": "Hırsızlık suçunda kast bakımından aşağıdakilerden hangisi doğrudur?",
        "secenekler": [
            "Taksirle işlenebilir",
            "Yalnızca olası kastla işlenebilir",
            "Kasten işlenebilir",
            "Yalnızca bilinçli taksirle işlenebilir",
            "Kusursuz sorumluluk esasına dayanır",
        ],
        "dogru_cevap": 2,
        "aciklama": "Hırsızlık suçu kasten işlenebilir; fail malı bilerek ve isteyerek almalıdır.",
        "kaynak": "TCK m.141",
        "zorluk": 2,
    },
    {
        "id": "CH_DOL_006",
        "dersadi": "Ceza Hukuku",
        "konu": "Dolandırıcılık Suçu",
        "soru": "Dolandırıcılık suçunda mağdurun iradesi nasıl etkilenir?",
        "secenekler": [
            "Cebir ile ortadan kaldırılır",
            "Tehdit ile baskı altına alınır",
            "Hile ile sakatlanır",
            "Tamamen serbest bırakılır",
            "Hukuken geçersiz sayılır",
        ],
        "dogru_cevap": 2,
        "aciklama": "Dolandırıcılıkta mağdur, hileli davranışlarla aldatılır ve iradesi sakatlanır.",
        "kaynak": "TCK m.157",
        "zorluk": 2,
    },
    {
        "id": "CH_DOL_007",
        "dersadi": "Ceza Hukuku",
        "konu": "Dolandırıcılık Suçu",
        "soru": "Dolandırıcılık suçunda fail hangi amaçla hareket eder?",
        "secenekler": [
            "Kamu düzenini sağlamak",
            "Hileyle menfaat sağlamak",
            "Mağduru cezalandırmak",
            "Malı zorla almak",
            "Zilyetliği geçici olarak devralmak",
        ],
        "dogru_cevap": 1,
        "aciklama": "Dolandırıcılıkta fail, hileli davranışlarla kendisine veya başkasına yarar sağlar.",
        "kaynak": "TCK m.157",
        "zorluk": 2,
    },
    {
        "id": "CH_GEN_003",
        "dersadi": "Ceza Hukuku",
        "konu": "Taksir",
        "soru": "Taksirin temel unsuru aşağıdakilerden hangisidir?",
        "secenekler": [
            "Bilerek hareket etmek",
            "Hileli davranışta bulunmak",
            "Dikkat ve özen yükümlülüğüne aykırılık",
            "Cebir kullanmak",
            "Menfaat sağlamak",
        ],
        "dogru_cevap": 2,
        "aciklama": "Taksir, dikkat ve özen yükümlülüğüne aykırılık sonucu istenmeyen neticenin meydana gelmesidir.",
        "kaynak": "Genel Hükümler",
        "zorluk": 2,
    },
    {
        "id": "CH_GEN_004",
        "dersadi": "Ceza Hukuku",
        "konu": "Taksir",
        "soru": "Bilinçli taksirde fail bakımından aşağıdakilerden hangisi doğrudur?",
        "secenekler": [
            "Netice hiç öngörülmez",
            "Netice istenir",
            "Netice öngörülür ancak gerçekleşmeyeceği düşünülür",
            "Netice zorla meydana getirilir",
            "Fail iradesizdir",
        ],
        "dogru_cevap": 2,
        "aciklama": "Bilinçli taksirde netice öngörülür ancak gerçekleşmeyeceği varsayılır.",
        "kaynak": "Genel Hükümler",
        "zorluk": 3,
    },
]

# Beklenti (kendin de kağıda yaz):
# - "Hırsızlık suçu nedir?" sorusu → 1-2-3 en yüksek, 4 orta-yüksek (aynı alan ceza), 5-6 orta,
#   7-8 düşük, 9-10 çok düşük çıkmalı.
