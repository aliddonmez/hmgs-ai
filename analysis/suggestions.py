##analysis/suggestions.py
def generate_study_suggestions(weak_topics):
    suggestions = []

    for t in weak_topics:
        konu = t["konu"]
        n_q = t["n_questions"]
        n_c = t["n_correct"]
        acc = t["accuracy"]
        status = t["data_status"]

        if status == "yetersiz":
            suggestions.append(
                f"{konu}: bu konuda henüz yeterli veri yok. "
                f"Biraz daha çalışıp soru çözerek analizi güçlendirebilirsin."
            )
            continue

        if acc < 40:
            suggestions.append(
                f"{konu}: doğruluk %{acc} ({n_c}/{n_q}). "
                f"Bu konuda zorlanıyorsun; temel kavramlara dönüp biraz daha çalışman ve soru çözmen faydalı olur."
            )
        elif acc < 70:
            suggestions.append(
                f"{konu}: doğruluk %{acc} ({n_c}/{n_q}). "
                f"Genel olarak fena değil; kısa bir tekrar ve birkaç soru çözmek yeterli olabilir."
            )
        else:
            suggestions.append(
                f"{konu}: doğruluk %{acc} ({n_c}/{n_q}). "
                f"Bu konuda durumun iyi görünüyor, mevcut seviyeni koruman yeterli."
            )

    return suggestions
