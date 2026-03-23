import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

import streamlit as st

st.set_page_config(page_title="HMGS", page_icon="⚖️")

st.title("HMGS – Hukuki Metin Asistanı")
st.divider()

page = st.sidebar.radio("Mod seç", ["Chat", "Quiz", "Dashboard"])

if page == "Chat":
    from app.ui.chat_page import render_chat
    render_chat()
elif page == "Quiz":
    from app.ui.quiz_page import render_quiz
    render_quiz()
elif page == "Dashboard":
    from app.ui.dashboard_page import render_dashboard
    render_dashboard()
