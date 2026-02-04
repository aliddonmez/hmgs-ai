# app/streamlit_app.py
import sys
import os

# -------------------------------------------------
# Proje root'unu path'e ekle
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

import streamlit as st

# -------------------------------------------------
# Streamlit config (İLK Streamlit çağrısı OLMALI)
# -------------------------------------------------
st.set_page_config(page_title="HMGS", page_icon="⚖️")

from app.rag_pipeline import run

# Quiz imports
from data.questions_v1 import questions
from app.quiz_engine import (
    start_quiz,
    get_current_question,
    submit_answer,
    is_finished,
    get_score,
    export_attempt_rows,
)
from app.sqlstorage import save_attempt_rows

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
page = st.sidebar.radio("Mod seç", ["Chat", "Quiz"])

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

    # Session init
    if "quiz_state" not in st.session_state:
        st.session_state.quiz_state = None

    if "quiz_saved" not in st.session_state:
        st.session_state.quiz_saved = False

    # Quiz başlat
    if st.button("Quiz'i Başlat"):
        st.session_state.quiz_state = start_quiz(questions)
        st.session_state.quiz_saved = False

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

            if st.button("🔄 Yeni Quiz Başlat"):
                st.session_state.quiz_state = start_quiz(questions)
                st.session_state.quiz_saved = False
                st.rerun()

        # ------------------------------
        # QUIZ DEVAM EDİYOR
        # ------------------------------
        else:
            st.markdown(f"### Soru {st.session_state.quiz_state['current_index'] + 1}")
            st.write(q["soru"])

            selected_text = st.radio("Şık seç", q["secenekler"], index=None)

            selected_index = None
            if selected_text is not None:
                selected_index = q["secenekler"].index(selected_text)

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
                        if result["dogru_mu"]:
                            st.success("✅ Doğru")
                        else:
                            st.error("❌ Yanlış")
                            st.info(f"ℹ️ {result.get('aciklama', '')}")

                        st.caption(f"Kaynak: {result.get('kaynak', '')}")
