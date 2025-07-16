import gradio as gr
import requests
import json
import time
import re
from typing import List, Tuple

# Configuration
API_URL = "http://localhost:8000/chat"  # Update with your actual URL
TITLE = "My AI Assistant"
THEME = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="gray",
).set(
    button_primary_background_fill="*primary_300",
    button_primary_background_fill_hover="*primary_200",
)

def query_chatbot(message: str, history: List[Tuple[str, str]], system_prompt: str, temperature: float, max_tokens: int):
    """Send user message to the chatbot API"""
    headers = {"Content-Type": "application/json"}
    payload = {
        "message": message,
        "history": history,
        "system_prompt": system_prompt,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Error: {str(e)}"

def format_response(response: str) -> str:
    """Format the response for better Markdown rendering"""
    # Improve Markdown list formatting
    response = re.sub(r'(\d+)\.\s', r'\1. ', response)  # Fix numbered lists
    response = re.sub(r'^\*\s', '- ', response, flags=re.MULTILINE)  # Convert * to - for bullet points
    
    # Improve code block formatting
    response = re.sub(r'```([^`]+)```', r'```\n\1\n```', response)
    
    # Improve section headers
    response = re.sub(r'^(\*{2}.+?\*{2})\s*$', r'## \1', response, flags=re.MULTILINE)
    
    return response

def user(user_message, history):
    """Add user message to history"""
    return "", history + [[user_message, None]]

def bot(history, system_prompt, temperature, max_tokens):
    """Get bot response and stream it with structured formatting"""
    # Get the last user message
    if not history or not history[-1][0]:
        return history
    
    # Prepare API history
    api_history = []
    for exchange in history[:-1]:
        if len(exchange) == 2 and exchange[1]:
            api_history.append((exchange[0], exchange[1]))
    
    # Get the assistant response
    assistant_response = query_chatbot(
        message=history[-1][0],
        history=api_history,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    # Format for better Markdown rendering
    assistant_response = format_response(assistant_response)
    
    history[-1][1] = ""
    for char in assistant_response:
        history[-1][1] += char
        time.sleep(0.01)  # Smooth streaming effect
        yield history

def regenerate(history, system_prompt, temperature, max_tokens):
    """Regenerate last bot response"""
    if history and history[-1][0]:
        history[-1][1] = None
        yield from bot(history, system_prompt, temperature, max_tokens)
    else:
        yield history

def undo(history):
    """Remove the last exchange"""
    if len(history) > 0:
        history.pop()
    return history

def clear_chat():
    """Clear the chat history"""
    return []

with gr.Blocks(theme=THEME, title=TITLE, css=".gradio-container {max-width: 800px !important}") as demo:
    gr.Markdown(f"## {TITLE}")
    
    # System prompt and parameters
    with gr.Accordion("⚙️ Parameters", open=False):
        system_prompt = gr.Textbox(
            label="System Prompt",
            value="You are a helpful AI assistant. Respond using Markdown formatting for lists, tables, and code blocks.",
            lines=3,
            placeholder="How should the assistant behave?"
        )
        with gr.Row():
            temperature = gr.Slider(0, 2, value=0.7, step=0.1, label="Temperature")
            max_tokens = gr.Slider(100, 4000, value=2000, step=100, label="Max Tokens")
    
    # Chat interface
    chatbot = gr.Chatbot(
        height=500,
        bubble_full_width=False,
        show_copy_button=True,
        avatar_images=("user.png", "bot.png"),  # Add your own avatar images
        render_markdown=True,  # Enable Markdown rendering
        sanitize_html=False  # Allow basic HTML formatting
    )
    
    # Message input
    msg = gr.Textbox(
        label="Message",
        placeholder="Type your message here...",
        container=False,
        autofocus=True
    )
    
    # Action buttons
    with gr.Row():
        submit_btn = gr.Button("Send", variant="primary")
        regen_btn = gr.Button("🔄 Regenerate")
        undo_btn = gr.Button("↩️ Undo")
        clear_btn = gr.Button("🗑️ Clear")
    
    # Event handlers
    msg.submit(
        user, [msg, chatbot], [msg, chatbot], queue=False
    ).then(
        bot, [chatbot, system_prompt, temperature, max_tokens], chatbot
    )
    
    submit_btn.click(
        user, [msg, chatbot], [msg, chatbot], queue=False
    ).then(
        bot, [chatbot, system_prompt, temperature, max_tokens], chatbot
    )
    
    regen_btn.click(
        regenerate, [chatbot, system_prompt, temperature, max_tokens], chatbot
    )
    
    undo_btn.click(undo, chatbot, chatbot)
    clear_btn.click(clear_chat, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.queue().launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        favicon_path="favicon.ico"  # Add your favicon
    )