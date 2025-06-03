import streamlit as st
import requests

# ---------- Page Config ----------
st.set_page_config(page_title="🧠 Mental Health Chatbot", layout="wide")

# ---------- Custom CSS ----------
def apply_custom_styles(dark_mode):
    base_bg = "#0f0f0f" if dark_mode else "#f9f9f9"
    user_bg = "#1e1e1e" if dark_mode else "#ffffff"
    bot_bg = "#222831" if dark_mode else "#e3f2fd"
    text_color = "#ffffff" if dark_mode else "#000000"

    st.markdown(f"""
    <style>
    body {{
        background-color: {base_bg};
        color: {text_color};
    }}
    .chat-bubble {{
        padding: 1rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }}
    .user-bubble {{
        background: linear-gradient(to right, #a1c4fd, #c2e9fb);
        text-align: left;
        color: black;
    }}
    .bot-bubble {{
        background: linear-gradient(to right, #d4fc79, #96e6a1);
        text-align: left;
        color: black;
    }}
    .emoji-radio .stRadio > div > label {{
        font-size: 1.2rem;
        margin-right: 10px;
    }}
    footer {{
        text-align: center;
        font-size: 0.85rem;
        margin-top: 30px;
        color: #777;
    }}
    </style>
    """, unsafe_allow_html=True)

# ---------- Session State ----------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- Sidebar Controls ----------
st.sidebar.markdown("## ⚙️ Chat Settings")
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=False)
apply_custom_styles(dark_mode)

tone = st.sidebar.selectbox("🗣️ Tone", ["Supportive", "Friendly", "Neutral"])
length = st.sidebar.radio("✏️ Response Length", ["Short", "Detailed"])
emotion = st.sidebar.radio("🧠 Current Emotion", ["😊", "😐", "😢", "😡"], key="emotion", horizontal=True)

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.history = []
    st.rerun()

# ---------- App Header ----------
st.markdown("""
<div style='text-align:center; padding-top: 10px;'>
    <h1 style='font-family:sans-serif;'>🧠 <span style='color:#5C6BC0'>Mental Health Chatbot</span></h1>
    <p style='font-size:1.1rem;'>You're not alone. Ask anything — <b>anonymously</b> and safely.</p>
    <p style='font-size:0.95rem;color:gray;'>Sometimes, just sharing how you feel is the first step toward healing.</p>
    <hr>
</div>
""", unsafe_allow_html=True)

# ---------- Empty State Message ----------
if len(st.session_state.history) == 0:
    st.markdown("""
    <div style="text-align:center; padding: 20px; color: #888;">
        <em>"Every day may not be good, but there's something good in every day."</em><br><br>
        👋 Start by telling me how you feel or what’s on your mind.
    </div>
    """, unsafe_allow_html=True)

# ---------- Chat History Display ----------
for chat in st.session_state.history:
    st.markdown(f"""
    <div class="chat-bubble user-bubble">
        <b>🧍 You:</b> {chat['user']}
    </div>
    <div class="chat-bubble bot-bubble">
        <b>🤖 Bot:</b> {chat['bot']}
    </div>
    """, unsafe_allow_html=True)

# ---------- Chat Input ----------
st.markdown("### 💬 What's on your mind?")
query = st.text_area("", height=100, placeholder="Type your thoughts, worries, or anything else...")

# ---------- Helper Text Below Input ----------
st.markdown("""
<p style='font-size:0.9rem; color:gray;'>📝 Tip: Try starting with something like “I feel overwhelmed because...” or “Lately, I’ve been thinking about...”</p>
""", unsafe_allow_html=True)

# ---------- Send Query ----------
if st.button("🕊️ Send"):
    if query.strip():
        with st.spinner("Thinking..."):
            payload = {
                "query": query,
                "history": st.session_state.history,
                "tone": tone,
                "length": length,
                "emotion": emotion
            }
            try:
                res = requests.post("http://localhost:8000/ask", json=payload)
                res.raise_for_status()
                answer = res.json()["response"]
                st.session_state.history.append({"user": query, "bot": answer})
                st.rerun()
            except requests.exceptions.RequestException as e:
                st.error(f"❌ API Error: {e}")

# ---------- Auto-scroll ----------
st.markdown("""
<script>
    const chatArea = window.parent.document.querySelector('.main');
    if (chatArea) {{
        chatArea.scrollTop = chatArea.scrollHeight;
    }}
</script>
""", unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("""
<footer>
    🤍 This chatbot is not a substitute for professional help. If you're in crisis, please reach out to a licensed therapist or a local mental health helpline.
</footer>
""", unsafe_allow_html=True)
