import streamlit as st
import requests
import json
import time
import os
from typing import List, Dict

# ========== CONFIGURATION ==========
# Use Docker container IP for backend
API_BASE_URL = os.getenv("BACKEND_URL", "http://172.18.45.183:8000")
TITLE = "🤖 AI Model Hub"
AVATARS = {"user": "👤", "assistant": "🤖"}

MODELS = {
    "gemini": {
        "name": "Gemini",
        "icon": "🌟",
        "system_prompt": "You are Gemini, Google's AI model.",
        "temperature": 0.7,
        "max_tokens": 2000,
        "model_param": "gemini"
    },
    "deepseek": {
        "name": "DeepSeek R1",
        "icon": "🤖",
        "system_prompt": "You are DeepSeek R1, a helpful AI assistant.",
        "temperature": 0.7,
        "max_tokens": 2000,
        "model_param": "deepseek",
        "disabled": True
    },
    "claude": {
        "name": "Claude",
        "icon": "👤",
        "system_prompt": "You are Claude, Anthropic's AI assistant.",
        "temperature": 0.7,
        "max_tokens": 2000,
        "model_param": "claude",
        "disabled": True
    },
    "gpt4": {
        "name": "GPT-4",
        "icon": "🧠",
        "system_prompt": "You are GPT-4, OpenAI's advanced AI model.",
        "temperature": 0.7,
        "max_tokens": 2000,
        "model_param": "gpt4",
        "disabled": True
    }
}

# ========== SESSION STATE ==========
def init_session_state():
    """Initialize session state variables"""
    if "current_model" not in st.session_state:
        st.session_state.current_model = "deepseek"
    
    if "models" not in st.session_state:
        st.session_state.models = {}
        for model_id, config in MODELS.items():
            st.session_state.models[model_id] = {
                "messages": [],
                "params": {
                    "system_prompt": config["system_prompt"],
                    "temperature": config["temperature"],
                    "max_tokens": config["max_tokens"]
                }
            }

# ========== API FUNCTIONS ==========
def query_chatbot(model_id: str, message: str, history: List[Dict[str, str]]) -> str:
    """Send user message to the chatbot API"""
    model_config = MODELS[model_id]
    params = st.session_state.models[model_id]["params"]
    
    payload = {
        "model": model_config["model_param"],
        "message": message,
        "history": history,
        "system_prompt": params["system_prompt"],
        "temperature": params["temperature"],
        "max_tokens": params["max_tokens"]
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat/",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=60
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        return f"🚨 API Error: {str(e)}"
    except Exception as e:
        return f"🚨 Unexpected Error: {str(e)}"

# ========== UI COMPONENTS ==========
def model_selector() -> None:
    """Display model selection sidebar"""
    with st.sidebar:
        st.title(TITLE)
        st.markdown("---")
        st.subheader("Available Models")
        
        for model_id, config in MODELS.items():
            disabled = config.get("disabled", False)
            btn_label = f"{config['icon']} {config['name']} {'🔴' if disabled else ''}"
            
            if st.button(
                btn_label,
                key=f"btn_{model_id}",
                use_container_width=True,
                disabled=disabled
            ):
                st.session_state.current_model = model_id
                st.rerun()
        
        st.markdown("---")
        show_model_settings()
        st.markdown("---")
        show_chat_controls()
        st.markdown("---")
        st.info(f"Backend URL: `{API_BASE_URL}`")

def show_model_settings() -> None:
    """Display settings for current model"""
    model_id = st.session_state.current_model
    config = MODELS[model_id]
    params = st.session_state.models[model_id]["params"]
    
    st.subheader(f"{config['icon']} {config['name']} Settings")
    
    with st.expander("⚙️ Configuration", expanded=True):
        params["system_prompt"] = st.text_area(
            "System Prompt",
            value=params["system_prompt"],
            height=150,
            help="How should the assistant behave?"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            params["temperature"] = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=2.0,
                value=params["temperature"],
                step=0.1,
                help="Higher values = more creative/random"
            )
        with col2:
            params["max_tokens"] = st.slider(
                "Max Tokens",
                min_value=100,
                max_value=4000,
                value=params["max_tokens"],
                step=100,
                help="Response length limit"
            )

def show_chat_controls() -> None:
    """Display chat management controls"""
    model_id = st.session_state.current_model
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.models[model_id]["messages"] = []
        st.rerun()

def display_chat(model_id: str) -> None:
    """Display chat messages for current model"""
    messages = st.session_state.models[model_id]["messages"]
    
    for msg in messages:
        avatar = AVATARS["assistant"] if msg["role"] == "assistant" else AVATARS["user"]
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# ========== MAIN PAGE ==========
def chat_interface() -> None:
    """Main chat interface"""
    model_id = st.session_state.current_model
    config = MODELS[model_id]
    
    # Display header
    st.header(f"{config['icon']} {config['name']}")
    st.caption(config.get("description", "AI Assistant"))
    
    # Display chat
    display_chat(model_id)
    
    # Handle user input
    if prompt := st.chat_input("Type your message..."):
        handle_user_input(model_id, prompt)

def handle_user_input(model_id: str, prompt: str) -> None:
    """Process user input and generate response"""
    # Add user message to history
    messages = st.session_state.models[model_id]["messages"]
    messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user", avatar=AVATARS["user"]):
        st.markdown(prompt)
    
    # Prepare API history in correct format
    history = []
    for msg in st.session_state.models[model_id]["messages"][:-1]:
        history.append({"role": msg["role"], "content": msg["content"]})
    
    # Generate and display assistant response
    with st.chat_message("assistant", avatar=AVATARS["assistant"]):
        response_placeholder = st.empty()
        full_response = ""
        
        # Get API response
        assistant_response = query_chatbot(
            model_id=model_id,
            message=prompt,
            history=history
        )
        
        # Stream response character by character
        for char in assistant_response:
            full_response += char
            time.sleep(0.01)
            response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
    
    # Add assistant response to history
    messages.append({"role": "assistant", "content": full_response})

# ========== APP CONFIGURATION ==========
def main():
    """Main application function"""
    st.set_page_config(
        page_title=TITLE,
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    init_session_state()
    model_selector()
    chat_interface()

if __name__ == "__main__":
    main()