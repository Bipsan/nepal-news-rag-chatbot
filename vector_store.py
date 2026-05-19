import os
import pandas as pd
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

CSV_FILE = "nepal_news.csv"
DB_LOCATION = "./nepal_news_db"


def build_vector_store(vector_store):
    df = pd.read_csv(CSV_FILE)
    print(f"⚙️  Chunking and embedding {len(df)} articles...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    documents = []
    ids = []
    chunk_index = 0

    for i, row in df.iterrows():
        full_text = row["title"] + "\n\n" + str(row["content"])
        chunks = splitter.split_text(full_text)
        for chunk in chunks:
            doc = Document(
                page_content=chunk,
                metadata={
                    "title": str(row.get("title", "")),
                    "date": str(row.get("date", "")),
                    "category": str(row.get("category", "")),
                    "url": str(row.get("url", "")),
                },
                id=str(chunk_index),
            )
            documents.append(doc)
            ids.append(str(chunk_index))
            chunk_index += 1

    print(f"✅ {len(df)} articles → {len(documents)} chunks")

    batch_size = 50
    for start in range(0, len(documents), batch_size):
        vector_store.add_documents(
            documents=documents[start:start + batch_size],
            ids=ids[start:start + batch_size],
        )
        print(f"  Embedded {min(start + batch_size, len(documents))}/{len(documents)}...")

    print("✅ Vector store built.\n")


def get_retriever():
    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(f"'{CSV_FILE}' not found. Run scraper.py first.")

    embeddings = OllamaEmbeddings(model="mxbai-embed-large")

    vector_store = Chroma(
        collection_name="nepal_news",
        embedding_function=embeddings,
        persist_directory=DB_LOCATION,
    )

    # Check if the collection actually has documents
    existing_count = vector_store._collection.count()

    if existing_count == 0:
        print("📭 Vector store is empty, building from CSV...")
        build_vector_store(vector_store)
    else:
        print(f"✅ Vector store loaded ({existing_count} chunks).\n")

    return vector_store.as_retriever(search_kwargs={"k": 5})


if __name__ == "__main__":
    get_retriever()
    print("Vector store ready.")