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
from app.sqlstorage import (
    save_attempt_rows,
    create_quiz_attempt,
    finalize_quiz_attempt,
)
from analysis.user_report import get_user_report


def render_quiz():

    questions = get_questions()

    user_id = st.text_input("Kullanıcı ID")

    if not user_id:
        st.warning("Kullanıcı ID gir.")
        return

    if "quiz_state" not in st.session_state:
        st.session_state.quiz_state = None

    if "quiz_saved" not in st.session_state:
        st.session_state.quiz_saved = False

    # ----------------------------
    # QUIZ AYARLARI
    # ----------------------------

    mode = st.selectbox("Quiz Modu", ["random", "balanced", "weak_focus"])

    n_questions = st.slider("Soru Sayısı", 5, 50, 20)

    weak_topic_input = None
    if mode == "weak_focus":
        weak_topic_input = st.text_input("Zayıf konu (isteğe bağlı)")

    # ----------------------------
    # QUIZ BAŞLAT
    # ----------------------------

    if st.button("Quiz'i Başlat"):

        report = get_user_report(user_id)
        weak_topic_names = [
            t.get("konu") for t in report.get("weak_topics", []) if t.get("konu")
        ]

        selected_questions = select_questions(
            question_pool=questions,
            n_questions=n_questions,
            mode=mode,
            weak_topics=weak_topic_names,
        )

        if not selected_questions:
            st.error("Bu ayarlara göre soru bulunamadı.")
            return

        st.session_state.quiz_state = start_quiz(selected_questions)
        create_quiz_attempt(
            attempt_id=st.session_state.quiz_state["attempt_id"],
            user_id=user_id,
            mode=mode,
            total_questions=len(st.session_state.quiz_state["questions"]),
            started_at=st.session_state.quiz_state["started_at"],
        )
        st.session_state.quiz_saved = False
        st.rerun()

    # ----------------------------
    # QUIZ AKIŞI
    # ----------------------------

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
            from datetime import datetime, timezone

            duration = (
                datetime.now(timezone.utc) - st.session_state.quiz_state["started_at"]
            ).total_seconds()

            finalize_quiz_attempt(
                attempt_id=st.session_state.quiz_state["attempt_id"],
                correct_count=st.session_state.quiz_state["score"],
                wrong_count=len(st.session_state.quiz_state["questions"])
                - st.session_state.quiz_state["score"],
                finished_at=datetime.now(timezone.utc),
                total_duration_seconds=int(duration),
            )

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
        st.rerun()
