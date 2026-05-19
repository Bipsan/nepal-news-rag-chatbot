import os
from scraper import run_scraper
from vector_store import get_retriever
from chat import run_chat

CSV_FILE = "nepal_news.csv"

if __name__ == "__main__":
    # Step 1 — scrape only if CSV doesn't exist yet
    if not os.path.exists(CSV_FILE):
        print("📰 No dataset found. Starting scraper...\n")
        run_scraper()
    else:
        print(f"📰 Dataset found ({CSV_FILE}), skipping scrape.\n")

    # Step 2 — embed into vector store (skipped automatically if DB exists)
    # Step 3 — start chat (get_retriever is called inside run_chat)
    run_chat()