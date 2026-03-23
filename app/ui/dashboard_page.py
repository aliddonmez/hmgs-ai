import streamlit as st
import pandas as pd
import plotly.express as px

from analysis.user_report import get_user_report


def render_dashboard():
    st.subheader("📊 Kullanıcı Performans Dashboard")

    user_id = st.text_input("User ID")

    if not user_id:
        st.info("Lütfen analiz için User ID girin.")
        return

    report = get_user_report(user_id)

    if not report:
        st.warning("Veri bulunamadı.")
        return

    summary = report.get("summary", {})
    weak_topics = report.get("weak_topics", [])
    strong_topics = report.get("strong_topics", [])
    insufficient_topics = report.get("insufficient_data_topics", [])
    suggestions = report.get("suggestions", [])

    # ---------------------------
    # KPI Kartları
    # ---------------------------
    col1, col2 = st.columns(2)

    col1.metric("📚 Total Questions", summary.get("total_questions", 0))
    col2.metric("🎯 Accuracy", f"%{summary.get('accuracy', 0)}")

    st.divider()

    # ---------------------------
    # Zayıf Konular
    # ---------------------------
    st.markdown("### ⚠️ Zayıf Konular")

    if weak_topics:
        df = pd.DataFrame(weak_topics)

        if "accuracy" in df.columns:
            df["accuracy"] = df["accuracy"].astype(float)

        fig = px.bar(
            df,
            x="konu",
            y="accuracy",
            title="Konu Bazlı Başarı Oranı",
            labels={"accuracy": "Başarı (%)", "konu": "Konu"},
            text="accuracy",
        )

        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(yaxis_range=[0, 100])

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 📋 Detaylı Performans")

        display_df = df[
            ["konu", "n_questions", "n_correct", "n_wrong", "accuracy"]
        ].rename(
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
    if strong_topics:
        st.markdown("### 💪 Güçlü Konular")

        strong_df = pd.DataFrame(strong_topics)

        st.dataframe(
            strong_df[["konu", "n_questions", "accuracy"]].rename(
                columns={
                    "konu": "Konu",
                    "n_questions": "Toplam",
                    "accuracy": "Başarı (%)",
                }
            ),
            use_container_width=True,
        )

    # ---------------------------
    # Veri Yetersiz Konular
    # ---------------------------
    if insufficient_topics:
        st.markdown("### ⚠️ Veri Yetersiz Konular")

        for t in insufficient_topics:
            st.warning(t.get("message", ""))

    # ---------------------------
    # Çalışma Önerileri
    # ---------------------------
    if suggestions:
        st.markdown("### 🧠 Çalışma Önerileri")

        for s in suggestions:
            st.info(s)
