# analysis/rank_topics.py


def rank_weak_topics(topic_stats: list[dict]) -> list[dict]:
    """
    Konu bazlı istatistik listesini zayıftan güçlüye doğru sıralar.

    Parametre:
    topic_stats:
        compute_topic_stats() fonksiyonundan gelen konu istatistikleri listesi.

        Beklenen örnek veri:
        [
            {
                "konu": "Ceza Hukuku",
                "n_questions": 10,
                "n_correct": 4,
                "n_wrong": 6,
                "accuracy": 40.0,
                "data_status": "yeterli"
            },
            {
                "konu": "Borçlar Hukuku",
                "n_questions": 2,
                "n_correct": 1,
                "n_wrong": 1,
                "accuracy": 50.0,
                "data_status": "yetersiz"
            }
        ]

    Dönen değer:
        Sıralanmış konu listesi.

        Mantık:
        1. Önce yeterli veriye sahip konular gelir.
        2. Yeterli konular kendi içinde düşük başarıdan yüksek başarıya sıralanır.
        3. Başarı oranı aynıysa daha fazla soru çözülmüş olan konu öne alınır.
        4. Veri yetersiz konular listenin sonuna eklenir.
    """

    # Yeterli veriye sahip konular burada tutulur.
    # Örneğin min_n = 3 ise ve kullanıcı o konuda en az 3 soru çözmüşse
    # bu konu "yeterli" kabul edilir.
    sufficient = []

    # Analiz için yeterli soru çözülmemiş konular burada tutulur.
    # Örneğin kullanıcı bir konuda sadece 1 soru çözmüşse
    # bu konu "yetersiz" kabul edilir.
    insufficient = []

    # -------------------------------------------------
    # 1) Konuları yeterli / yetersiz olarak ayır
    # -------------------------------------------------
    for t in topic_stats:

        # data_status değeri "yeterli" ise bu konu analiz edilebilir.
        if t["data_status"] == "yeterli":
            sufficient.append(t)

        # data_status "yetersiz" ise bu konu sağlıklı analiz için sona alınır.
        else:
            insufficient.append(t)

    # -------------------------------------------------
    # 2) Yeterli konuları zayıflığa göre sırala
    # -------------------------------------------------
    # Sıralama mantığı:
    #
    # key=lambda x: (x["accuracy"], -x["n_questions"])
    #
    # 1. Önce accuracy küçük olan öne gelir.
    #    Örneğin:
    #    %30 başarı, %70 başarıdan önce gelir.
    #
    # 2. Eğer accuracy eşitse, daha çok soru çözülmüş olan öne gelir.
    #    Bunun için -x["n_questions"] kullanılır.
    #
    #    Örnek:
    #    A konusu: %50 başarı, 10 soru
    #    B konusu: %50 başarı, 3 soru
    #
    #    A konusu daha güvenilir veri içerdiği için önce gelir.
    sufficient_sorted = sorted(
        sufficient,
        key=lambda x: (x["accuracy"], -x["n_questions"])
    )

    # -------------------------------------------------
    # 3) Yetersiz verileri listenin sonuna ekle
    # -------------------------------------------------
    # Yetersiz konuları başa koymuyoruz çünkü bu konularda gerçek bir zayıflık
    # olup olmadığını söylemek için yeterli veri yok.
    #
    # Örnek:
    # Kullanıcı bir konuda 1 soru çözüp yanlış yaptıysa başarı %0 çıkar.
    # Ama tek soruya bakarak "bu konu çok zayıf" demek doğru olmaz.
    return sufficient_sorted + insufficient