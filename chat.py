from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector_store import get_retriever

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
template = """
You are a knowledgeable assistant on Nepali current affairs and news.
Answer the question using ONLY the news articles provided below.
If the articles don't contain enough information to answer, say so honestly.
Always mention the date and category of the article(s) you referenced.

Relevant articles:
{articles}

Question: {question}
"""


# ─────────────────────────────────────────────
# Chat loop
# ─────────────────────────────────────────────
def run_chat():
    print("🔢 Loading vector store...")
    retriever = get_retriever()

    model = OllamaLLM(model="llama3.2")
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    print("💬 Nepal News RAG Agent ready! Ask me anything about recent Nepali news.")
    print("   Type 'q' to quit.\n")

    while True:
        print("-" * 50)
        question = input("Your question: ").strip()
        print("-" * 50)

        if question.lower() == "q":
            print("Goodbye!")
            break

        if not question:
            continue

        articles = retriever.invoke(question)
        result = chain.invoke({"articles": articles, "question": question})
        print(f"\n{result}\n")


if __name__ == "__main__":
    run_chat()