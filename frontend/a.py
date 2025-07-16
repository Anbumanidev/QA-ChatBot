import streamlit as st
import requests

st.set_page_config(page_title="Simple Chatbot", layout="centered")

st.markdown("""
<style>
.chat-container {
    height: 400px;
    overflow-y: auto;
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 10px;
    background-color: #f9f9f9;
    border-radius: 10px;
    scroll-behavior: smooth;
}
.chat-bubble {
    display: inline-block;
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 15px;
    max-width: 80%;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    margin-bottom: 8px;
    color: #000;
}
.user {
    background-color: #aee1f9;
    float: right;
    clear: both;
    text-align: right;
}
.bot {
    background-color: #e6f4ea;
    float: left;
    clear: both;
    text-align: left;
}
.stTextInput > div > div > input {
    color: #000 !important;
    background-color: #fff !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## 💬 Simple Chatbot")

API_URL = "http://127.0.0.1:8000/chat"  # Your backend API

def get_bot_response(message):
    # Replace with your actual API call
    try:
        response = requests.post(API_URL, json={"message": message})
        if response.status_code == 200:
            return response.json().get("response", "No response from server.")
        else:
            return f"Error: {response.status_code} {response.text}"
    except Exception as e:
        return f"Error: {e}"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def submit():
    user_msg = st.session_state.user_input.strip()
    if user_msg:
        st.session_state.chat_history.append(("You", user_msg))
        bot_reply = get_bot_response(user_msg)
        st.session_state.chat_history.append(("Bot", bot_reply))
        st.session_state.user_input = ""

# Display chat history inside a scrollable container
chat_html = "<div class='chat-container'>"
for speaker, msg in st.session_state.chat_history:
    if speaker == "You":
        chat_html += f"<div class='chat-bubble user'><b>🧑 You:</b> {msg}</div>"
    else:
        chat_html += f"<div class='chat-bubble bot'><b>🤖 Bot:</b> {msg}</div>"
# Invisible anchor to scroll into view
chat_html += "<div id='scroll-anchor'></div></div>"

st.markdown(chat_html, unsafe_allow_html=True)

st.text_input("Type your message...", key="user_input", on_change=submit)

# Scroll to the anchor div to always show latest messages
st.markdown("""
<script>
const anchor = window.parent.document.getElementById('scroll-anchor');
if(anchor){
    anchor.scrollIntoView({behavior: 'smooth'});
}
</script>
""", unsafe_allow_html=True)
