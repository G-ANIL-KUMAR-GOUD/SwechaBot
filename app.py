import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# -------------------------------
# Load chatbot model from Hugging Face
# -------------------------------
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# -------------------------------
# Streamlit Page Configuration
# -------------------------------
st.set_page_config(page_title="🤖 Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 AI Chatbot")
st.markdown("Welcome! Chat with the *DialoGPT-medium* model below.")

# -------------------------------
# Chat History Initialization
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = None
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of (role, text)

# -------------------------------
# User Input
# -------------------------------
with st.container():
    user_input = st.text_area("💬 Type your message:", height=80)
    col1, col2 = st.columns([1, 0.3])
    with col1:
        send = st.button("🚀 Send")
    with col2:
        clear = st.button("🗑 Clear Chat")

# Clear Chat Button
if clear:
    st.session_state.chat_history = None
    st.session_state.messages = []
    st.experimental_rerun()

# -------------------------------
# Chatbot Response
# -------------------------------
if send and user_input.strip():
    # Convert user message to tokens
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")

    # Add previous conversation context
    if st.session_state.chat_history is not None:
        input_ids = torch.cat([st.session_state.chat_history, input_ids], dim=-1)

    # Generate reply
    response_ids = model.generate(
        input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id
    )
    response = tokenizer.decode(
        response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True
    )

    # Save history
    st.session_state.chat_history = response_ids
    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("Bot", response))

# -------------------------------
# Display Chat Messages
# -------------------------------
st.markdown("### 💭 Conversation")
chat_box = st.container()

if st.session_state.messages:
    for role, msg in st.session_state.messages:
        if role == "You":
            chat_box.markdown(
                f"<div style='text-align:right; color:white; background-color:#4CAF50; padding:8px; border-radius:10px; margin:5px 0; display:inline-block;'>{msg}</div>",
                unsafe_allow_html=True,
            )
        else:
            chat_box.markdown(
                f"<div style='text-align:left; color:black; background-color:#f1f0f0; padding:8px; border-radius:10px; margin:5px 0; display:inline-block;'>{msg}</div>",
                unsafe_allow_html=True,
            )