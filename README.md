# Nepal News RAG Chatbot

A local Retrieval-Augmented Generation (RAG) chatbot for Nepali current affairs and news.

This project:
- scrapes news from Kathmandu Post,
- creates vector embeddings,
- stores semantic search indexes using ChromaDB,
- and answers user questions using a local LLM powered by Ollama.

---

# Features

- News scraping with Playwright
- Semantic search with vector embeddings
- Chroma vector database
- Local LLM inference using Ollama
- Fully offline RAG pipeline
- Metadata-aware retrieval
- Automatic dataset/vector DB initialization

---

# Tech Stack

- Python
- LangChain
- Ollama
- Llama 3.2
- ChromaDB
- Playwright
- Pandas

---

# Project Structure

```text
.
├── chat.py
├── main.py
├── scraper.py
├── vector_store.py
├── nepal_news.csv
├── requirements.txt
├── README.md
└── .gitignore
```

---

# How It Works

```text
Kathmandu Post
       ↓
Web Scraping
       ↓
Structured Dataset (CSV)
       ↓
Text Chunking
       ↓
Embeddings
       ↓
Chroma Vector DB
       ↓
Retriever
       ↓
Llama 3.2
       ↓
AI Chatbot
```

---

# Setup

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/nepal-news-rag-chatbot.git
cd nepal-news-rag-chatbot
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install Playwright Browsers

```bash
playwright install
```

---

## 5. Install Ollama

Download and install:

https://ollama.com

---

## 6. Pull Required Models

### Embedding model

```bash
ollama pull mxbai-embed-large
```

### Chat model

```bash
ollama pull llama3.2
```

---

# Run the Project

```bash
python main.py
```

The application will:

1. Check if dataset exists
2. Scrape news automatically if needed
3. Build vector database automatically if needed
4. Start the chatbot

---

# Example Questions

```text
What happened in Nepal politics recently?

Summarize the latest economic news.

What are the recent national issues in Nepal?
```

---

# RAG Architecture

This project implements:

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Embeddings
- Local LLM Inference

---

# Future Improvements

- Conversation memory
- Streamlit UI
- FastAPI backend
- Source citations
- Streaming responses
- Hybrid search
- Async scraping

---

# License

MIT License