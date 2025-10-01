import os
import shutil
import re
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

CHROMA_DIR = os.path.join("db", "chroma_db")
DATA_DIR = "data"


def load_documents():
    """Load only the 2011 Act TXT file."""
    docs = []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".txt") and "2011" in file:   # ✅ only 2011 Act
            path = os.path.join(DATA_DIR, file)
            loader = TextLoader(path, encoding="utf-8")
            loaded = loader.load()
            for d in loaded:
                d.metadata["source_file"] = file
            docs.extend(loaded)
    return docs


def split_text(documents):
    """Split text into chunks by sections/parts/clauses for legal accuracy."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=100,
        separators=["Schedule ", "Clause ", "Part ", "Division ", "Section ", "\n\n", "\n"]
    )
    chunks = splitter.split_documents(documents)

    # Anchored regex patterns (match only at start of line)
    section_re = re.compile(r"^Section\s+\d+[A-Z]?", re.IGNORECASE | re.MULTILINE)
    part_re = re.compile(r"^Part\s+\d+(\.\d+)?", re.IGNORECASE | re.MULTILINE)
    schedule_re = re.compile(r"^Schedule\s+\d+", re.IGNORECASE | re.MULTILINE)
    clause_re = re.compile(r"^Clause\s+\d+", re.IGNORECASE | re.MULTILINE)

    current_schedule = None

    for ch in chunks:
        text = ch.page_content

        # Detect schedule heading
        if m := schedule_re.search(text):
            current_schedule = m.group(0)
            ch.metadata["schedule"] = current_schedule

        # Detect clause (highest priority)
        if m := clause_re.search(text):
            clause_text = m.group(0)
            if current_schedule:
                ch.metadata["schedule"] = current_schedule
            ch.metadata["clause"] = clause_text
            continue  # ✅ don’t also assign "section"

        # Only detect sections if no clause heading
        if m := section_re.search(text):
            ch.metadata["section"] = m.group(0)

        # Detect part
        if m := part_re.search(text):
            ch.metadata["part"] = m.group(0)

        # Carry forward current schedule
        if "schedule" not in ch.metadata and current_schedule:
            ch.metadata["schedule"] = current_schedule

    print(f"📑 Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks


def build_db():
    # Clean old DB
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    docs = load_documents()
    chunks = split_text(docs)

    # Embeddings + Chroma
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    db.persist()
    print(f"✅ Built new Chroma DB with {len(chunks)} chunks at {CHROMA_DIR}")


if __name__ == "__main__":
    build_db()
