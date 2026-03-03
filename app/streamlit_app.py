# app/streamlit_app.py
import sys
import os

# -------------------------------------------------
# Proje root'unu path'e ekle
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from collections import Counter  # ✅ DEBUG için eklendi

# -------------------------------------------------
# Streamlit config (İLK Streamlit çağrısı OLMALI)
# -------------------------------------------------
st.set_page_config(page_title="HMGS", page_icon="⚖️")

from app.rag_pipeline import run
from app.question_select import select_questions

# Quiz imports
from app.repositories.questions_repo import get_questions

questions = get_questions()

from app.quiz_engine import (
    start_quiz,
    get_current_question,
    submit_answer,
    is_finished,
    get_score,
    export_attempt_rows,
)

from app.sqlstorage import save_attempt_rows

# Dashboard / Analysis import
from analysis.user_report import get_user_report

# Grafik için (13.7)
import matplotlib.pyplot as plt


def _get_lesson_name(q: dict) -> str:
    """Hem eski (dersadi) hem yeni (ders) veriye uyumluluk."""
    return q.get("ders") or q.get("dersadi") or "Bilinmiyor"


# -------------------------------------------------
# UI HEADER
# -------------------------------------------------
st.title("HMGS – Hukuki Metin Asistanı")

st.markdown(
    "Bu sistem, yalnızca mevcut ve güvenilir hukuki kaynaklara dayanarak cevap üretir. "
    "Gerekli durumlarda bilinçli olarak cevap vermeyebilir."
)

st.divider()

# -------------------------------------------------
# SAYFA SEÇİMİ
# -------------------------------------------------
page = st.sidebar.radio("Mod seç", ["Chat", "Quiz", "Dashboard"])


# =================================================
# CHAT
# =================================================
if page == "Chat":
    question = st.chat_input("Sorunuzu yazın")

    if question:
        with st.chat_message("user"):
            st.markdown(question)

        result = run(question)

        with st.chat_message("assistant"):
            if result.get("type") == "no_answer":
                st.info(
                    "### Bu soruda durduk\n\n"
                    "İlgili ve güvenilir hukuki kaynaklar bulunamadığı için "
                    "bu soruya cevap üretmedik."
                )
                st.caption(
                    "Yanlış veya eksik yönlendirme yapmamak için cevap vermemek tercih edilmiştir."
                )
                st.caption(f"reason: {result.get('reason')}")
            else:
                st.markdown(result.get("text", ""))
                st.caption("Bu cevap, mevcut hukuki kaynaklara dayanarak üretilmiştir.")


# =================================================
# QUIZ
# =================================================
elif page == "Quiz":
    st.subheader("Quiz")

    # Kullanıcı ID
    user_id = st.text_input("Kullanıcı ID", placeholder="ör: ali_donmez")

    if not user_id:
        st.warning("Sonuçları kaydedebilmemiz için lütfen bir kullanıcı ID gir.")
        st.stop()

    st.caption(f"Kullanıcı: {user_id}")

    # ✅ Debug panel toggle
    show_debug = st.checkbox("🛠 Debug göster", value=True)

    # Quiz türü seçimi
    quiz_mode_label = st.radio(
        "Quiz Türünü Seç",
        [
            "🧠 Otomatik (Zayıf Konulara Göre)",
            "⚖ Dengeli",
            "🎲 Rastgele",
        ],
    )

    st.caption("Otomatik mod, zayıf konularınıza daha fazla soru getirir.")

    # Session init
    if "quiz_state" not in st.session_state:
        st.session_state.quiz_state = None

    if "quiz_saved" not in st.session_state:
        st.session_state.quiz_saved = False

    # ---------------------------------------------
    # QUIZ BAŞLAT
    # ---------------------------------------------
    if st.button("Quiz'i Başlat"):
        if quiz_mode_label == "🧠 Otomatik (Zayıf Konulara Göre)":
            report = get_user_report(user_id)
            weak_topic_names = [t.get("konu") for t in report.get("weak_topics", []) if t.get("konu")]
            mode = "weak_focus"

        elif quiz_mode_label == "⚖ Dengeli":
            weak_topic_names = []
            mode = "balanced"

        else:
            weak_topic_names = []
            mode = "random"

        selected_questions = select_questions(
            question_pool=questions,
            n_questions=20,
            mode=mode,
            weak_topics=weak_topic_names,
            seed=42,
        )

        # ✅ DEBUG: seçilen soruların dağılımını göster
        if show_debug:
            ders_sayim = Counter(_get_lesson_name(q) for q in selected_questions)
            konu_sayim = Counter(q.get("konu") or "Bilinmiyor" for q in selected_questions)

            st.write("✅ Seçilen Quiz Modu:", mode)
            st.write("📚 Ders dağılımı:", dict(ders_sayim))
            st.write("📌 Konu dağılımı:", dict(konu_sayim))

            if weak_topic_names:
                weak3 = weak_topic_names[:3]
                weak_count = sum(1 for q in selected_questions if q.get("konu") in weak3)
                st.write("🧠 Weak topics (ilk 3):", weak3)
                st.write("🧠 Weak soru sayısı:", f"{weak_count} / {len(selected_questions)}")

        st.session_state.quiz_state = start_quiz(selected_questions)
        st.session_state.quiz_saved = False
        st.rerun()

    # -------------------------------------------------
    # QUIZ AKIŞI
    # -------------------------------------------------
    if st.session_state.quiz_state is not None:
        q = get_current_question(st.session_state.quiz_state)

        # ------------------------------
        # QUIZ BİTTİ
        # ------------------------------
        if q is None or is_finished(st.session_state.quiz_state):
            if not st.session_state.quiz_saved:
                rows = export_attempt_rows(
                    st.session_state.quiz_state,
                    user_id=user_id,
                )
                save_attempt_rows(rows)
                st.session_state.quiz_saved = True

            score = get_score(st.session_state.quiz_state)
            st.success(f"🎉 Quiz bitti! Skor: {score['score']} / {score['total']}")

            # ---------------------------------------------
            # YENİ QUIZ (SEÇİLEN MODLA)
            # ---------------------------------------------
            if st.button("🔄 Yeni Quiz Başlat"):
                if quiz_mode_label == "🧠 Otomatik (Zayıf Konulara Göre)":
                    report = get_user_report(user_id)
                    weak_topic_names = [
                        t.get("konu") for t in report.get("weak_topics", []) if t.get("konu")
                    ]
                    mode = "weak_focus"

                elif quiz_mode_label == "⚖ Dengeli":
                    weak_topic_names = []
                    mode = "balanced"

                else:
                    weak_topic_names = []
                    mode = "random"

                selected_questions = select_questions(
                    question_pool=questions,
                    n_questions=20,
                    mode=mode,
                    weak_topics=weak_topic_names,
                    seed=42,
                )

                # ✅ DEBUG: yeni quiz için de dağılım
                if show_debug:
                    ders_sayim = Counter(_get_lesson_name(q) for q in selected_questions)
                    konu_sayim = Counter(q.get("konu") or "Bilinmiyor" for q in selected_questions)

                    st.write("✅ Seçilen Quiz Modu:", mode)
                    st.write("📚 Ders dağılımı:", dict(ders_sayim))
                    st.write("📌 Konu dağılımı:", dict(konu_sayim))

                    if weak_topic_names:
                        weak3 = weak_topic_names[:3]
                        weak_count = sum(1 for q in selected_questions if q.get("konu") in weak3)
                        st.write("🧠 Weak topics (ilk 3):", weak3)
                        st.write("🧠 Weak soru sayısı:", f"{weak_count} / {len(selected_questions)}")

                st.session_state.quiz_state = start_quiz(selected_questions)
                st.session_state.quiz_saved = False
                st.rerun()

        # ------------------------------
        # QUIZ DEVAM EDİYOR
        # ------------------------------
        else:
            st.markdown(f"### Soru {st.session_state.quiz_state['current_index'] + 1}")

            # Soru metni
            st.write(q.get("question", ""))

            # Şıklar
            options = q.get("options", [])
            selected_text = st.radio("Şık seç", options, index=None)

            selected_index = None
            if selected_text is not None:
                selected_index = options.index(selected_text)

            if st.button("Cevabı Gönder"):
                if selected_index is None:
                    st.warning("Lütfen bir şık seç.")
                else:
                    result = submit_answer(
                        st.session_state.quiz_state,
                        selected_index,
                    )

                    if "error" in result:
                        st.warning(result["error"])
                    else:
                        if result.get("dogru_mu"):
                            st.success("✅ Doğru")
                        else:
                            st.error("❌ Yanlış")
                            st.info(f"ℹ️ {result.get('aciklama', '')}")

                        st.caption(f"Kaynak: {result.get('kaynak', '')}")

                    st.rerun()


# =================================================
# DASHBOARD (Gün 13 - B)
# =================================================
elif page == "Dashboard":
    st.subheader("Dashboard")

    # 13.6 - User ID input (+ opsiyonel buton)
    dash_user_id = st.text_input("User ID", placeholder="ör: ali_donmez", key="dash_user_id")

    # Basit cache: aynı user_id için tekrar hesaplamayı azaltır (13.3)
    if "report_cache" not in st.session_state:
        st.session_state.report_cache = {}

    # Raporu getir butonu (opsiyonel)
    fetch_clicked = st.button("Raporu getir")

    if not dash_user_id:
        st.info("Dashboard görmek için bir User ID gir.")
        st.stop()

    # Eğer butona basılmadıysa da gösterebiliriz,
    # ama senin isteğine göre: butonla çalışsın istersen bu satırı aç/kapat.
    if not fetch_clicked and dash_user_id not in st.session_state.report_cache:
        st.info("Raporu görmek için “Raporu getir” butonuna bas.")
        st.stop()

    # Raporu cache’ten al veya yeniden üret
    try:
        if fetch_clicked or dash_user_id not in st.session_state.report_cache:
            st.session_state.report_cache[dash_user_id] = get_user_report(dash_user_id)

        report = st.session_state.report_cache.get(dash_user_id)

    except Exception as e:
        st.error("Rapor oluşturulurken hata oluştu.")
        st.caption(f"Hata: {e}")
        st.stop()

    if not report:
        st.warning("Bu kullanıcı için rapor bulunamadı.")
        st.stop()

    # 13.8 - veri yok / eksik durumlarını düzgün anlat
    summary = report.get("summary", {})
    total_q = summary.get("total_questions", 0)

    if total_q == 0:
        st.warning("Bu kullanıcı için henüz kayıt yok. Önce quiz çözmelisin.")
        st.stop()

    # 13.6 - Üst metrik kutuları
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Questions", summary.get("total_questions", 0))
    col2.metric("Accuracy", f"%{summary.get('accuracy', 0)}")
    col3.metric("Correct / Wrong", f"{summary.get('correct', 0)} / {summary.get('wrong', 0)}")

    st.divider()

    # 13.6 - En zayıf konular (Top 5)
    weak_topics = report.get("weak_topics", [])[:5]
    st.markdown("### 📉 En zayıf konular (Top 5)")
    if not weak_topics:
        st.info("Zayıf konu listesi üretilemedi.")
    else:
        for t in weak_topics:
            st.write(f"- {t.get('konu', '-')}: %{t.get('accuracy', 0)} ({t.get('n_questions', 0)} soru)")

    # 13.6 - En güçlü konular (Top 3)
    strong_topics = report.get("strong_topics", [])[:3]
    st.markdown("### 💪 En güçlü konular (Top 3)")
    if not strong_topics:
        st.info("Güçlü konu listesi üretilemedi.")
    else:
        for t in strong_topics:
            st.write(f"- {t.get('konu', '-')}: %{t.get('accuracy', 0)} ({t.get('n_questions', 0)} soru)")

    # 13.4 - Yetersiz veri uyarısı
    insufficient = report.get("insufficient_data_topics", [])
    if insufficient:
        st.markdown("### ⚠️ Yetersiz veri olan konular")
        for t in insufficient:
            st.write(f"- {t.get('konu', '-')}: sadece {t.get('n', 0)} soru (analiz için az)")

    st.divider()

    # 13.7 - Basit grafik: konu bazlı doğruluk (Top 10)
    st.markdown("### 📊 Konu bazlı doğruluk (Top 10)")
    topic_stats = report.get("topic_stats", [])
    if topic_stats:
        # En çok soru çözülen ilk 10 konuyu göster
        sorted_by_n = sorted(topic_stats, key=lambda x: x.get("n_questions", 0), reverse=True)[:10]
        labels = [x.get("konu", "-") for x in sorted_by_n]
        values = [x.get("accuracy", 0) for x in sorted_by_n]

        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_ylabel("Accuracy (%)")
        ax.set_ylim(0, 100)
        plt.xticks(rotation=35, ha="right")
        st.pyplot(fig)
    else:
        st.info("Grafik için yeterli konu istatistiği yok.")

    st.divider()

    # 13.6 - Öneriler
    st.markdown("### 🧠 Öneriler")
    suggestions = report.get("suggestions", [])
    if not suggestions:
        st.info("Öneri üretilemedi.")
    else:
        for s in suggestions:
            st.write(f"- {s}")