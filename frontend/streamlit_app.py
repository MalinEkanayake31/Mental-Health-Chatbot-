import streamlit as st
import requests

st.set_page_config(page_title="Mental Health Chatbot")
st.title("🧠 Mental Health Chatbot")
st.markdown("You're not alone. Ask anything — **anonymously** and safely.")

# Session state for chat
if "history" not in st.session_state:
    st.session_state.history = []

# Display past messages
for chat in st.session_state.history:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**Bot:** {chat['bot']}")

# Input area
query = st.text_area("What's on your mind?", height=100)

# Send button
if st.button("Send"):
    if query.strip():
        with st.spinner("Thinking..."):
            res = requests.post("http://localhost:8000/ask", json={
                "query": query,
                "history": st.session_state.history
            })
            answer = res.json()["response"]
            st.session_state.history.append({"user": query, "bot": answer})
            st.rerun()


# Optional clear chat
if st.button("🧹 Clear Chat"):
    st.session_state.history = []
    st.rerun()

