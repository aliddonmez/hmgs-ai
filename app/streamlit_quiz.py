import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)


import streamlit as st


##quiz motoru ve fonksiyonlarını import ediyoruz .
from quiz_engine import (
    start_quiz,  ## başlangıç durumunu oluşturur . 
    get_current_question, ## mevcut soruyu döndürür . 
    submit_answer,  #doğru yanlış kontrolü yapılır , skor verilir , sonraki soruya geçiş sağlanır . 
    is_finished, # bitiş kontrolü 
    get_score # scor sonucu 
)


# sorularımızın importu
from data.questions_v1 import questions as QUESTIONS

##streamlit her girişte scripti yeniden başlatır . 
##started: quiz başladı mı?
##quiz_state: quiz motorunun tuttuğu state (questions, current_index, score, answers vb.)
##last_feedback: en son cevap sonrası gösterilecek “doğru/yanlış + açıklama” paketi
if "started" not in st.session_state:
    st.session_state.started = False

if "quiz_state" not in st.session_state:
    st.session_state.quiz_state = None

if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = None


# -----------------------------
# UI
# -----------------------------
st.title(" Quiz")

# ---- QUIZ BAŞLAT ----
if not st.session_state.started:
    st.write("Hazırsan quiz’e başlayabilirsin.")
    if st.button(" Quiz’i Başlat"):
        st.session_state.quiz_state = start_quiz(QUESTIONS) ##state üretilir .
        st.session_state.started = True ##quiz ekranına geçilecek .
        st.session_state.last_feedback = None ##eski mesaj kalmasın 
        st.rerun()

# ---- QUIZ AKIŞI ----
else:
    state = st.session_state.quiz_state

    # Quiz bittiyse
    if is_finished(state):
        result = get_score(state)

        st.success(" Quiz tamamlandı!")
        st.write(f"Skor: **{result['score']} / {result['total']}**")

        st.divider()
        st.write("Cevapların kaydedildi. Analiz edilebilir.")

    else:
        question = get_current_question(state)

        # ---- META (şimdilik sade) ----
        st.caption(
            f"{question['dersadi']} · {question['konu']} · Zorluk: {question['zorluk']}"
        )

        # ---- SORU ----
        st.subheader(question["soru"])

        # ---- SEÇENEKLER ---- aslında index seçiyor 
        selected_option = st.radio(
            "Seçenekler:",
            options=list(range(len(question["secenekler"]))),
            format_func=lambda x: question["secenekler"][x],
            key=f"q_{state['current_index']}"
        )

        # ---- CEVABI GÖNDER ----
        if st.button(" Cevabı Gönder"):
            feedback = submit_answer(state, selected_option)
            st.session_state.last_feedback = feedback
            st.rerun()

        # ---- GERİ BİLDİRİM ----
        if st.session_state.last_feedback:
            fb = st.session_state.last_feedback

            if fb.get("dogru_mu"):
                st.success(" Doğru")
            else:
                st.error(" Yanlış")

            if fb.get("aciklama"):
                st.info(fb["aciklama"])

            if fb.get("kaynak"):
                st.caption(f" Kaynak: {fb['kaynak']}")
