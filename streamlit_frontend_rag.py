import streamlit as st
import os
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import google.generativeai as genai
import pathlib
import datetime

today = datetime.date.today().isoformat()

# Path to the API key file
api_key_path = os.path.join("config", "google_api")
try:
    with open(api_key_path, "r") as f:
        api_key = f.read().strip()
except FileNotFoundError:
    api_key = None

if not api_key:
    st.error("⚠️ Gemini API key not found. Please place it in config/.env or directly in the code.")
    st.stop()

genai.configure(api_key=api_key)

@st.cache_resource(show_spinner=True)
def load_faiss():
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    base_dir = pathlib.Path(__file__).parent.resolve()
    index_path = base_dir / "embeddings" / "faiss_index_hf"

    if not index_path.exists():
        st.error(f"FAISS index not found at {index_path}")
        st.stop()

    index = FAISS.load_local(
        str(index_path),
        embedding_model,
        allow_dangerous_deserialization=True
    )
    return index

faiss_index = load_faiss()

def ask_gemini(query, top_k=5):
    results = faiss_index.similarity_search(query, k=top_k)
    if not results:
        return "No relevant documents found."

    context = "\n\n".join([r.page_content for r in results])
    prompt = f"""You are Vincenzo Colella's personal assistant. You only reply using information found in the provided context. The context contains excerpts from personal documents, events, notes, reminders, and other user-related data. The question is: {query}

- Only use information in the context to answer.
- If the question asks for events or time-based details, extract only what's relevant, and note that today is {today}.
- Keep the answer precise and cheerful, with a friendly tone and emojis when appropriate.

Here is the context:
{context}
Answer:"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text or "The model did not generate a response."

# Function to manage session chat and log user questions to file
def add_message(role, content):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    st.session_state.chat_history.append({"role": role, "content": content})
    if role == "user":
        with open("log_questions.txt", "a", encoding="utf-8") as f:
            f.write(content.strip() + "\n")

# Page setup and style
st.set_page_config(
    page_title="Vincenzo Colella's Personal Assistant 🤖",
    page_icon="🤵‍♂️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f0f2f6, #d9e2f3);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .chat-message {
        padding: 12px 16px;
        margin-bottom: 10px;
        border-radius: 12px;
        max-width: 75%;
        word-wrap: break-word;
        font-size: 16px;
        line-height: 1.4;
    }
    .user-message {
        background-color: #4a90e2;
        color: white;
        margin-left: auto;
    }
    .bot-message {
        background-color: #e4e7f0;
        color: #333;
        margin-right: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤵‍♂️ Vincenzo Personal Assistant")
st.write(
    "Ask questions about Vincenzo's documents, events, reminders, and more. "
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("✍️ Enter your question:", key="input_box")

submit_disabled = not user_input.strip()

if st.button("🚀 Send", disabled=submit_disabled):
    add_message("user", user_input)
    with st.spinner("🤖 Generating response..."):
        try:
            response = ask_gemini(user_input)
        except Exception as e:
            response = f"❌ Error generating response: {e}"
        add_message("bot", response)

# Display chat (bot and user messages, not in sidebar)
for msg in reversed(st.session_state.chat_history):
    css_class = "user-message" if msg["role"] == "user" else "bot-message"
    st.markdown(f'<div class="chat-message {css_class}">{msg["content"]}</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("© 2025 Vincenzo Colella — Powered by HuggingFace, FAISS and Gemini Flash LLM 🤖")

# Easter egg: show questions after 10 clicks
if "easter_egg_counter" not in st.session_state:
    st.session_state.easter_egg_counter = 0

if st.button("🕹️", key="easter_button"):
    st.session_state.easter_egg_counter += 1

if st.session_state.easter_egg_counter >= 10:
    st.success("🎉 You unlocked the easter egg!")
    try:
        with open("log_questions.txt", "r", encoding="utf-8") as f:
            questions = f.readlines()
        st.markdown("### 📜 Logged Questions:")
        for question in questions:
            st.markdown(f"- {question.strip()}")
    except FileNotFoundError:
        st.error("The file 'log_questions.txt' was not found.")
