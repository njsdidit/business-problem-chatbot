import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# ------------ Configuration ------------
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL = os.getenv("MODEL", "gpt-4o-mini")

if not API_KEY:
    st.error("Please set OPENAI_API_KEY in your .env file")
    st.stop()

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

SYSTEM_PROMPT = """You are a practical real-time business problem solver.
Help the user quickly with clear, actionable advice on:
- Operations & process issues
- Customer problems
- Sales & marketing decisions
- Inventory / supply chain
- Team / productivity issues
- Simple financial or pricing questions

Be concise, structured, and solution-oriented.
Ask clarifying questions only when necessary.
When useful, give step-by-step actions the user can take right now.
"""

# ------------ Streamlit UI ------------
st.set_page_config(page_title="Business Problem Solver", page_icon="💼", layout="centered")
st.title("💼 Real-Time Business Problem Solver")
st.caption("Describe any business problem and get practical help instantly.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Describe your business problem..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages,
                    temperature=0.4,
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")

# Sidebar
with st.sidebar:
    st.header("About")
    st.write("Simple AI assistant for real-time business problems.")
    st.write("Built with Streamlit + OpenAI-compatible API.")
    
    if st.button("Clear conversation"):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()
