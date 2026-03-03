import streamlit as st
from analysis.user_report import get_user_report


def render_dashboard():

    user_id = st.text_input("User ID")

    if not user_id:
        st.info("User ID gir.")
        return

    report = get_user_report(user_id)

    summary = report.get("summary", {})

    st.metric("Total Questions", summary.get("total_questions", 0))
    st.metric("Accuracy", f"%{summary.get('accuracy', 0)}")

    weak_topics = report.get("weak_topics", [])
    st.write("Zayıf konular:", weak_topics)
