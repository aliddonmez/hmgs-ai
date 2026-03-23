import streamlit as st
from app.rag_pipeline import run


def render_chat():
    import streamlit as st

    st.subheader("HMGS Hukuki Asistan")
    st.write("Aşağıya hukuki bir soru yazın.")

    # session state başlat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # geçmiş mesajları göster
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # yeni soru
    question = st.chat_input("Sorunuzu yazın")

    if question:

        # kullanıcı mesajını kaydet
        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.markdown(question)

        result = run(question)

        if result.get("type") == "no_answer":
            answer = "İlgili güvenilir kaynak bulunamadı."
        else:
            answer = result.get("text", "")

        # assistant mesajını kaydet
        st.session_state.messages.append({"role": "assistant", "content": answer})

        with st.chat_message("assistant"):
            st.markdown(answer)
