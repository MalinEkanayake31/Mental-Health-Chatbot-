import streamlit as st
import requests

# App setup
st.set_page_config(page_title="Mental Health Chatbot", layout="centered")
st.markdown("""
    <h1 style="text-align: center;">🧠 Mental Health Chatbot</h1>
    <p style="text-align: center;">You're not alone. Ask anything — <strong>anonymously</strong> and safely.</p>
    <hr>
""", unsafe_allow_html=True)

# Session state for conversation
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar options
st.sidebar.header("🛠️ Chat Settings")
tone = st.sidebar.selectbox("Tone of Response", ["Supportive", "Friendly", "Neutral"])
length = st.sidebar.radio("Response Length", ["Short", "Detailed"])
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.history = []
    st.rerun()

# Render chat history
for i, chat in enumerate(st.session_state.history):
    st.markdown(f"""
    <div style="background-color:#f0f0f5;padding:10px;border-radius:10px;margin-bottom:10px;">
        <b>🧍 You:</b> {chat['user']}
    </div>
    <div style="background-color:#e8f5e9;padding:10px;border-radius:10px;margin-bottom:20px;">
        <b>🤖 Bot:</b> {chat['bot']}
    </div>
    """, unsafe_allow_html=True)

# Chat input
query = st.text_area("💬 What's on your mind?", height=100)

# Send button
if st.button("🕊️ Send"):
    if query.strip():
        with st.spinner("Thinking..."):
            # Sending query and settings to backend
            payload = {
                "query": query,
                "history": st.session_state.history,
                "tone": tone,
                "length": length
            }
            try:
                res = requests.post("http://localhost:8000/ask", json=payload)
                res.raise_for_status()
                answer = res.json()["response"]
                st.session_state.history.append({"user": query, "bot": answer})
                st.rerun()
            except requests.exceptions.RequestException as e:
                st.error(f"❌ API Error: {e}")
