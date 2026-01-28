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
# Streamlit config (İLK Streamlit çağrısı OLMALI) sayfa başlığı ve icon 
# -------------------------------------------------
st.set_page_config(page_title="HMGS", page_icon="⚖️")


from app.rag_pipeline import run 
##Kullanıcı soru sorunca, arka planda çalışan RAG sistemi run(question) fonksiyonu ile cevap üretecek.


st.title("HMGS – Hukuki Metin Asistanı")

st.markdown(
    "Bu sistem, yalnızca mevcut ve güvenilir hukuki kaynaklara dayanarak cevap üretir. "
    "Gerekli durumlarda bilinçli olarak cevap vermeyebilir."
)

st.divider() ##ekrana yatay çizgi 

# -------------------------------------------------
# CHAT
# -------------------------------------------------
question = st.chat_input("Sorunuzu yazın")

if question:
    with st.chat_message("user"):
        st.markdown(question)

    result = run(question)

    with st.chat_message("assistant"):

        # 🟡 BİLİNÇLİ SUSMA
        if result.get("type") == "no_answer":
            st.info(
                "### Bu soruda durduk\n\n"
                "İlgili ve güvenilir hukuki kaynaklar bulunamadığı için "
                "bu soruya cevap üretmedik.\n\n"
                "Bu, sistemin bilinçli bir tercihidir."
            )

            st.caption(
                "Yanlış veya eksik yönlendirme yapmamak için cevap vermemek tercih edilmiştir."
            )

        # 🟢 NORMAL CEVAP
        else:
            st.markdown(result.get("text", ""))

            st.caption(
                "Bu cevap, mevcut hukuki kaynaklara dayanarak üretilmiştir."
            )
