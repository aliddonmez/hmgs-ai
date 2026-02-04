def rank_weak_topics(topic_stats: list[dict]) -> list[dict]:
    """
    ##konu listesi alır konu listesi sıralanmış şekilde gelir .
    Konuları zayıflıktan güçlüye doğru sıralar.
    """

    sufficient = []  ##yeterliler
    insufficient = []  ##yetersizler

    # 1) Yeterli / yetersiz ayır
    for t in topic_stats:
        if t["data_status"] == "yeterli":
            sufficient.append(t)
        else:
            insufficient.append(t)

    # 2) Zayıflık sıralaması
    sufficient_sorted = sorted(
        sufficient, key=lambda x: (x["accuracy"], -x["n_questions"])
    )

    ##Önce accuracy küçük olanı öne al,Eğer accuracy aynıysa: daha çok soru çözülmüş olanı öne al.

    # 3) Yetersiz verileri sona ekle
    return sufficient_sorted + insufficient
