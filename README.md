# 🧠 RAG Application on Personal Documents
This application was developed to query personal documents such as PDFs, Word files, and Google Calendars using natural language, through a RAG (Retrieval-Augmented Generation) system. The goal is to allow users to ask questions and receive answers based on their own personal data.

## 🔍 What the Application Does
Loads documents from a folder (PDF and DOCX).

Extracts textual content from these files.

Generates semantic embeddings (i.e., vector representations of the meaning of the texts).

Saves these embeddings in a FAISS index, allowing fast retrieval of the most relevant documents in response to a question.

When the user writes a question, the app searches for the most relevant documents and sends them to the language model to generate a response.

## 🧱 Technology Stack Used
Python: main development language.

Streamlit: to quickly and easily build the web interface.

FAISS (Facebook AI Similarity Search): to store and query the vector index of the documents.

Language Models (via Hugging Face or OpenAI): to generate natural language responses.

PyMuPDF / python-docx: to read the content of PDF and Word files.

Google Calendar API (optional): to load and query calendar events.

dotenv: for secure API key management.

Pandas, NumPy, etc.: for data handling and general support.

## ▶️ How to Use It
Place your files in the data/ folder.

The app automatically generates a vector index on first run.

Access a simple web interface where you can type your question.

The app responds using only the information found in your documents.

## 📁 Project Structure (Simplified)

rag_vincenzo/
├── app.py              # Streamlit application
├── data/               # Documents to be analyzed
├── embeddings/         # Generated FAISS index
├── utils/              # Functions to read files, create embeddings, etc.
└── requirements.txt    # List of required libraries
## 📌 Important Notes
If the FAISS index is not present, the app generates it automatically.

The interface is designed for personal and local use, not for production.

You can easily modify the embedding models or the document sources.

## ✍️ Author
Developed by Vincenzo Colella
Data Engineer, Switzerland









