# app/ui/dashboard_page.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Kullanıcı performans raporunu oluşturan fonksiyon
from analysis.user_report import get_user_report


def render_dashboard():
    """
    Kullanıcı performans dashboard ekranını oluşturur.

    Bu ekran:
    - User ID alır
    - Kullanıcının çözüm geçmişini analiz eder
    - Genel başarı özetini gösterir
    - Zayıf konuları grafik ve tablo halinde gösterir
    - Güçlü konuları listeler
    - Veri yetersiz konuları uyarı olarak gösterir
    - Statik/kural tabanlı çalışma önerilerini gösterir
    """

    # Sayfa başlığı
    st.subheader("📊 Kullanıcı Performans Dashboard")

    # Analiz yapılacak kullanıcı ID değeri alınır
    user_id = st.text_input("User ID")

    # User ID boşsa işlem yapılmaz
    if not user_id:
        st.info("Lütfen analiz için User ID girin.")
        return

    # Girilen kullanıcı ID için performans raporu oluşturulur
    report = get_user_report(user_id)

    # Rapor boş dönerse veri bulunamadı mesajı gösterilir
    if not report:
        st.warning("Veri bulunamadı.")
        return

    # Rapor içindeki ana bölümler alınır
    summary = report.get("summary", {})
    weak_topics = report.get("weak_topics", [])
    strong_topics = report.get("strong_topics", [])
    insufficient_topics = report.get("insufficient_data_topics", [])
    suggestions = report.get("suggestions", [])

    # Summary içindeki değerler güvenli şekilde alınır
    total_questions = summary.get("total_questions", 0)
    correct = summary.get("correct", 0)
    wrong = summary.get("wrong", 0)
    accuracy = summary.get("accuracy", 0)

    # ---------------------------
    # KPI Kartları
    # ---------------------------
    # 4 kolon ile genel performans özeti gösterilir:
    # toplam soru, doğru, yanlış, başarı oranı
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📚 Toplam Soru", total_questions)
    col2.metric("✅ Doğru", correct)
    col3.metric("❌ Yanlış", wrong)
    col4.metric("🎯 Başarı", f"%{accuracy}")

    st.divider()

    # Kullanıcı hiç soru çözmemişse grafik ve detay bölümlerine geçmeye gerek yok
    if total_questions == 0:
        st.info("Bu kullanıcı için henüz analiz yapılacak çözüm verisi yok.")
        return

    # ---------------------------
    # Zayıf Konular
    # ---------------------------
    st.markdown("### ⚠️ Zayıf Konular")

    if weak_topics:
        # Zayıf konular liste formatından DataFrame'e çevrilir
        df = pd.DataFrame(weak_topics)

        # accuracy kolonu sayısal tipe çevrilir
        if "accuracy" in df.columns:
            df["accuracy"] = df["accuracy"].astype(float)

        # Zayıf konular için bar grafik oluşturulur
        fig = px.bar(
            df,
            x="konu",
            y="accuracy",
            title="Zayıf Konulara Göre Başarı Oranı",
            labels={
                "accuracy": "Başarı (%)",
                "konu": "Konu",
            },
            text="accuracy",
        )

        # Barların üzerine başarı yüzdesi yazılır
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")

        # Y ekseni yüzde olduğu için 0-100 aralığına sabitlenir
        fig.update_layout(yaxis_range=[0, 100])

        # Grafik ekrana basılır
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 📋 Detaylı Zayıf Konu Performansı")

        # Tabloda gösterilecek kolonlar
        display_columns = [
            "konu",
            "n_questions",
            "n_correct",
            "n_wrong",
            "accuracy",
        ]

        # Kolon eksikliği olursa uygulama patlamasın diye sadece mevcut kolonlar seçilir
        existing_columns = [c for c in display_columns if c in df.columns]

        display_df = df[existing_columns].rename(
            columns={
                "konu": "Konu",
                "n_questions": "Toplam",
                "n_correct": "Doğru",
                "n_wrong": "Yanlış",
                "accuracy": "Başarı (%)",
            }
        )

        st.dataframe(display_df, use_container_width=True)

    else:
        st.success("Zayıf konu bulunmuyor 🎉")

    st.divider()

    # ---------------------------
    # Güçlü Konular
    # ---------------------------
    st.markdown("### 💪 Güçlü Konular")

    if strong_topics:
        strong_df = pd.DataFrame(strong_topics)

        display_columns = [
            "konu",
            "n_questions",
            "n_correct",
            "n_wrong",
            "accuracy",
        ]

        existing_columns = [c for c in display_columns if c in strong_df.columns]

        strong_display_df = strong_df[existing_columns].rename(
            columns={
                "konu": "Konu",
                "n_questions": "Toplam",
                "n_correct": "Doğru",
                "n_wrong": "Yanlış",
                "accuracy": "Başarı (%)",
            }
        )

        st.dataframe(strong_display_df, use_container_width=True)

    else:
        st.info("Güçlü konu bulunmuyor.")

    st.divider()

    # ---------------------------
    # Veri Yetersiz Konular
    # ---------------------------
    st.markdown("### ⚠️ Veri Yetersiz Konular")

    if insufficient_topics:
        for t in insufficient_topics:
            st.warning(t.get("message", "Bu konuda yeterli veri yok."))
    else:
        st.success("Veri yetersiz konu bulunmuyor.")

    st.divider()

    # ---------------------------
    # Çalışma Önerileri
    # ---------------------------
    st.markdown("### 🧠 Çalışma Önerileri")

    if suggestions:
        for s in suggestions:
            st.info(s)
    else:
        st.info("Şu an gösterilecek çalışma önerisi bulunmuyor.")