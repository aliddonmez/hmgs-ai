# analysis/suggestions.py


def generate_study_suggestions(weak_topics):
    """
    Kullanıcının zayıf olduğu konulara göre statik/kural tabanlı öneriler üretir.

    Bu fonksiyon yapay zeka kullanmaz.
    Kararlar tamamen kullanıcının konu bazlı başarı oranına göre verilir.

    Kural mantığı:
    - %40 altı  -> ciddi zayıflık
    - %40-%70   -> orta düzey eksik
    - %70 üstü -> iyi seviye

    Parametre:
    weak_topics:
        Kullanıcının zayıf olduğu konu listesi.

        Beklenen örnek veri:
        {
            "konu": "Ceza Hukuku",
            "n_questions": 10,
            "n_correct": 4,
            "n_wrong": 6,
            "accuracy": 40.0,
            "data_status": "yeterli"
        }

    Dönen değer:
    suggestions:
        Dashboard'da veya CLI raporda gösterilecek öneri metinleri listesi.
    """

    # Önerilerin tutulacağı liste
    suggestions = []

    # Zayıf konular tek tek gezilir
    for t in weak_topics:

        # Konu adı alınır.
        # Eğer konu bilgisi gelmezse "Bilinmeyen konu" yazılır.
        konu = t.get("konu", "Bilinmeyen konu")

        # Bu konuda çözülen toplam soru sayısı
        n_q = t.get("n_questions", 0)

        # Bu konuda doğru yapılan soru sayısı
        n_c = t.get("n_correct", 0)

        # Bu konudaki başarı yüzdesi
        acc = t.get("accuracy", 0)

        # Konu için veri durumu
        # Örnek değerler:
        # "yeterli"
        # "yetersiz"
        status = t.get("data_status", "yeterli")

        # Eğer konu için veri yetersizse öneri farklı verilir.
        #
        # Not:
        # Şu an user_report.py tarafında generate_study_suggestions()
        # sadece weak listesiyle çağrıldığı için bu blok çoğu zaman çalışmaz.
        # Çünkü "yetersiz" konular user_report.py içinde insufficient listesine ayrılıyor.
        if status == "yetersiz":
            suggestions.append(
                f"{konu}: bu konuda henüz yeterli veri yok. "
                f"Biraz daha çalışıp soru çözerek analizi güçlendirebilirsin."
            )
            continue

        # Başarı oranı %40'ın altındaysa ciddi zayıflık kabul edilir.
        # Bu durumda kullanıcıya temel konu tekrarı önerilir.
        if acc < 40:
            suggestions.append(
                f"{konu}: doğruluk %{acc} ({n_c}/{n_q}). "
                f"Bu konuda zorlanıyorsun; temel kavramlara dönüp biraz daha çalışman "
                f"ve açıklamalı soru çözmen faydalı olur."
            )

        # Başarı oranı %40 ile %70 arasındaysa orta düzey eksik kabul edilir.
        # Bu durumda kısa tekrar + ek soru çözümü önerilir.
        elif acc < 70:
            suggestions.append(
                f"{konu}: doğruluk %{acc} ({n_c}/{n_q}). "
                f"Genel olarak fena değil; kısa bir tekrar ve birkaç soru çözmek yeterli olabilir."
            )

        # Başarı oranı %70 ve üzerindeyse iyi seviye kabul edilir.
        #
        # Not:
        # Şu an user_report.py weak listesine genellikle %60 altı konuları gönderiyor.
        # Bu yüzden bu blok mevcut akışta çok sık çalışmayabilir.
        else:
            suggestions.append(
                f"{konu}: doğruluk %{acc} ({n_c}/{n_q}). "
                f"Bu konuda durumun iyi görünüyor, mevcut seviyeni koruman yeterli."
            )

    # Eğer zayıf konu yoksa genel bir öneri verilir.
    # Bu, kullanıcının dashboard'da boş öneri alanı görmesini engeller.
    if not suggestions:
        suggestions.append(
            "Belirgin bir zayıf konu görünmüyor. Mevcut seviyeyi korumak için "
            "düzenli tekrar ve karma test çözümü yapabilirsin."
        )

    # Oluşturulan öneriler döndürülür
    return suggestions