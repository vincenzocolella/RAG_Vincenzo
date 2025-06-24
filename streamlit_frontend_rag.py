import streamlit as st
import os
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import google.generativeai as genai
import pathlib
import datetime



today = datetime.date.today().isoformat()



# Percorso al file della chiave
api_key_path = os.path.join("config", "google_api")
try:
    with open(api_key_path, "r") as f:
        api_key = f.read().strip()
except FileNotFoundError:
    api_key = None

if not api_key:
    st.error("⚠️ Chiave API Gemini non trovata. Inseriscila in config/.env o nel codice.")
    st.stop()

genai.configure(api_key=api_key)

@st.cache_resource(show_spinner=True)
def load_faiss():
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    base_dir = pathlib.Path(__file__).parent.resolve()
    index_path = base_dir / "embeddings" / "faiss_index_hf"

    if not index_path.exists():
        st.error(f"Indice FAISS non trovato in {index_path}")
        st.stop()

    index = FAISS.load_local(
        str(index_path),
        embedding_model,
        allow_dangerous_deserialization=True
    )
    return index

faiss_index = load_faiss()

def ask_gemini(query, top_k=5):
    risultati = faiss_index.similarity_search(query, k=top_k)
    if not risultati:
        return "Nessun documento rilevante trovato."

    contesto = "\n\n".join([r.page_content for r in risultati])
    prompt = f""" Sei l'assistente personale di Vincenzo Colella che risponde solo utilizzando le informazioni presenti nel contesto fornito. Il contesto contiene estratti di documenti personali, eventi, note, promemoria e altre informazioni relative all'utente. La domanda è: {query} - Usa solo i dati presenti nel contesto per formulare la risposta. - Se la domanda richiede di elencare eventi o dettagli temporali, estrai solo quelli rilevanti, e considera che oggi è {today}. - Mantieni la risposta precisa e allegra, con un tono amichevole e emoji quando appropriato. Ecco il contesto: {contesto} Risposta: """
    modello = genai.GenerativeModel("gemini-1.5-flash")
    risposta = modello.generate_content(prompt)
    return risposta.text or "Il modello non ha generato una risposta."

# Funzione per gestire la chat in sessione e salvare domande su file
def add_message(role, content):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    st.session_state.chat_history.append({"role": role, "content": content})
    if role == "user":
        with open("log_domande.txt", "a", encoding="utf-8") as f:
            f.write(content.strip() + "\n")

# Setup pagina e stile
st.set_page_config(
    page_title="Assistant personale di Vincenzo Colella 🤖",
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

st.title("🤵‍♂️ Assistente personale di Vincenzo Colella")
st.write(
    "Fai domande sui tuoi documenti personali, eventi, promemoria e altro. "
    "Ricevi risposte basate sui tuoi dati indicizzati."
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("✍️ Inserisci la domanda:", key="input_box")

submit_disabled = not user_input.strip()

if st.button("🚀 Invia", disabled=submit_disabled):
    add_message("user", user_input)
    with st.spinner("🤖 Sto elaborando la risposta..."):
        try:
            risposta = ask_gemini(user_input)
        except Exception as e:
            risposta = f"❌ Errore nella generazione della risposta: {e}"
        add_message("bot", risposta)
# Visualizza chat (solo risposte del bot e domande, ma senza mostrarle in sidebar)
for msg in reversed(st.session_state.chat_history):
    css_class = "user-message" if msg["role"] == "user" else "bot-message"
    st.markdown(f'<div class="chat-message {css_class}">{msg["content"]}</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("© 2025 Vincenzo Colella — Powered by HuggingFace, FAISS e Gemini Flash LLM 🤖")
