# Nepal News RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built using:

- Playwright
- LangChain
- ChromaDB
- Ollama
- Llama 3.2

## Features

- Scrapes Nepal news articles
- Creates vector embeddings
- Stores semantic search index
- Local AI chatbot for Nepali news queries

## Tech Stack

- Python
- LangChain
- ChromaDB
- Ollama
- Playwright

## Setup

```bash
pip install -r requirements.txt
```

Run scraper:

```bash
python scraper.py
```

Build vector DB:

```bash
python vector_store.py
```

Run chatbot:

```bash
python chat.py
```