import os
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

CHROMA_DIR = os.path.join("db", "chroma_db")


def get_retriever():
    """Return a hybrid retriever (BM25 + Embedding)."""
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # Load Chroma DB
    db = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

    # Semantic retriever
    embedding_retriever = db.as_retriever(search_kwargs={"k": 6})

    # Keyword retriever (BM25)
    docs = db.get(include=["documents", "metadatas"])
    bm25_retriever = BM25Retriever.from_texts(
        texts=docs["documents"],
        metadatas=docs["metadatas"]
    )

    # Hybrid retriever (semantic weighted higher than keyword)
    hybrid = EnsembleRetriever(
        retrievers=[bm25_retriever, embedding_retriever],
        weights=[0.3, 0.7]
    )

    return hybrid


if __name__ == "__main__":
    retriever = get_retriever()
    print("✅ Hybrid Retriever ready")

    query = "balcony repairs"
    results = retriever.get_relevant_documents(query)
    for i, doc in enumerate(results, 1):
        # Build reference string
        schedule = doc.metadata.get("schedule")
        clause = doc.metadata.get("clause")
        section = doc.metadata.get("section")
        part = doc.metadata.get("part")

        if schedule and clause:
            reference = f"{schedule}, {clause}"
        elif schedule:
            reference = schedule
        elif part:
            reference = part
        elif section:
            reference = section
        else:
            reference = "Unknown"

        print(f"\n--- Result {i} ---")
        print("Reference:", reference)
        print(doc.page_content[:300], "...")
