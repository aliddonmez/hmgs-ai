import streamlit as st
from app.rag_pipeline import run


def render_chat():
    question = st.chat_input("Sorunuzu yazın")

    if question:
        with st.chat_message("user"):
            st.markdown(question)

        result = run(question)

        with st.chat_message("assistant"):
            if result.get("type") == "no_answer":
                st.info("İlgili güvenilir kaynak bulunamadı.")
            else:
                st.markdown(result.get("text", ""))
