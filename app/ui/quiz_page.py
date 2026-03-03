import streamlit as st
from collections import Counter

from app.repositories.questions_repo import get_questions
from app.question_select import select_questions
from app.quiz_engine import (
    start_quiz,
    get_current_question,
    submit_answer,
    is_finished,
    get_score,
    export_attempt_rows,
)
from app.sqlstorage import save_attempt_rows
from analysis.user_report import get_user_report

questions = get_questions()


def render_quiz():

    user_id = st.text_input("Kullanıcı ID")

    if not user_id:
        st.warning("Kullanıcı ID gir.")
        return

    if "quiz_state" not in st.session_state:
        st.session_state.quiz_state = None

    if "quiz_saved" not in st.session_state:
        st.session_state.quiz_saved = False

    if st.button("Quiz'i Başlat"):

        report = get_user_report(user_id)
        weak_topic_names = [
            t.get("konu") for t in report.get("weak_topics", []) if t.get("konu")
        ]

        selected_questions = select_questions(
            question_pool=questions,
            n_questions=20,
            mode="weak_focus",
            weak_topics=weak_topic_names,
            seed=42,
        )

        st.session_state.quiz_state = start_quiz(selected_questions)
        st.session_state.quiz_saved = False
        st.rerun()

    if st.session_state.quiz_state is None:
        return

    q = get_current_question(st.session_state.quiz_state)

    if q is None or is_finished(st.session_state.quiz_state):

        if not st.session_state.quiz_saved:
            rows = export_attempt_rows(
                st.session_state.quiz_state,
                user_id=user_id,
            )
            save_attempt_rows(rows)
            st.session_state.quiz_saved = True

        score = get_score(st.session_state.quiz_state)
        st.success(f"Skor: {score['score']} / {score['total']}")
        return

    st.write(q.get("question", ""))

    options = q.get("options", [])
    selected_text = st.radio("Şık seç", options, index=None)

    if st.button("Cevabı Gönder"):

        if selected_text is None:
            st.warning("Şık seç.")
            return

        selected_index = options.index(selected_text)

        result = submit_answer(
            st.session_state.quiz_state,
            selected_index,
        )

        if result.get("dogru_mu"):
            st.success("Doğru")
        else:
            st.error("Yanlış")
