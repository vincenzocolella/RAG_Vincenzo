# 🧠 Applicazione RAG su documenti personali

Questa applicazione è stata sviluppata per interrogare documenti personali come PDF, file Word e calendari Google in linguaggio naturale, utilizzando un sistema di **RAG (Retrieval-Augmented Generation)**. L'obiettivo è permettere all'utente di porre domande e ricevere risposte basate sui propri dati personali.

---

## 🔍 Cosa fa l'applicazione

1. Carica documenti da una cartella (PDF e DOCX).
2. Estrae il contenuto testuale da questi file.
3. Genera **embedding semantici** (cioè rappresentazioni vettoriali del significato dei testi).
4. Salva questi embedding in un **indice FAISS**, che consente di ritrovare velocemente i documenti più rilevanti rispetto a una domanda.
5. Quando l'utente scrive una domanda, l'app cerca nei documenti quelli più pertinenti e li invia al modello di linguaggio per generare una risposta.

---

## 🧱 Stack tecnologico utilizzato

- **Python**: linguaggio principale per lo sviluppo.
- **Streamlit**: per creare l’interfaccia web in modo semplice e veloce.
- **FAISS** (Facebook AI Similarity Search): per salvare e interrogare l’indice vettoriale dei documenti.
- **Modelli di linguaggio** (via Hugging Face o OpenAI): per generare le risposte in linguaggio naturale.
- **PyMuPDF / python-docx**: per leggere il contenuto di file PDF e Word.
- **Google Calendar API** (opzionale): per caricare e interrogare anche eventi del calendario.
- **dotenv**: per la gestione delle chiavi API in modo sicuro.
- **Pandas, NumPy, etc.**: per la gestione dei dati e supporto generale.

---

## ▶️ Come si usa

1. Si mettono i propri file nella cartella `data/`.
2. L’app genera automaticamente un indice vettoriale alla prima esecuzione.
3. Si accede a una semplice interfaccia web dove si può scrivere una domanda.
4. L'app risponde usando solo le informazioni presenti nei tuoi documenti.

---

## 📁 Struttura del progetto (semplificata)

rag_vincenzo/
├── app.py # applicazione Streamlit
├── data/ # documenti da analizzare
├── embeddings/ # indice FAISS generato
├── utils/ # funzioni per leggere file, creare embedding, ecc.
└── requirements.txt # librerie usate


---

## 📌 Note importanti

- Se non è presente l’indice FAISS, l’app lo crea automaticamente.
- L’interfaccia è pensata per uso personale e locale, non in produzione.
- Puoi modificare facilmente i modelli di embedding o la sorgente dei documenti.

---

## ✍️ Autore

Sviluppato da **Vincenzo Colella**  
Lead Data Engineer, Svizzera  
