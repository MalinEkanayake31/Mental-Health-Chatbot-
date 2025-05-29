import streamlit as st
import requests

st.set_page_config(page_title="Mental Health Chatbot")
st.title("🧠 Mental Health Chatbot")
st.markdown("You're not alone. Ask anything — **anonymously** and safely.")

query = st.text_area("What's on your mind?", height=100)

if st.button("Send"):
    if query.strip():
        with st.spinner("Thinking..."):
            res = requests.post("http://localhost:8000/ask", json={"query": query})
            st.success(res.json()["response"])
