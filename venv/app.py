import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("Please set GROQ_API_KEY in your environment")
    st.stop()

# Streamlit page configuration
st.set_page_config(page_title="Chatbot using Groq", page_icon="🧠")
st.title("Groq API based Chatbot 🧠 - Ayushi")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# User input
prompt = st.chat_input("Ask me anything!")

if prompt:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # Prepare request headers and body
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "model": "llama-3.1-8b-instant",  # <-- Valid Groq model
        "messages": st.session_state.messages
    }

    # Call Groq API
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=body,
    )

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        # Add assistant reply to session state
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").markdown(reply)
    else:
        st.error(f"Error {response.status_code}: {response.text}")
