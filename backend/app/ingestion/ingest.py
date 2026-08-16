"""
Phase 2: Ingestion Pipeline for PrepGPT

Run this script standalone (not part of the FastAPI app) whenever you add
or update documents in interview_prep_docs/.

Usage (from the backend/ folder):
    python -m app.ingestion.ingest
"""

import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"  # silence ChromaDB telemetry noise

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# --- Paths (relative to backend/ so run this from inside backend/) ---
DOCS_PATH = "./interview_prep_docs"
DB_PATH = "./chroma_db"
COLLECTION_NAME = "interview_prep"


def load_documents():
    """Load all markdown files from the docs folder."""
    loader = DirectoryLoader(
        DOCS_PATH,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )
    documents = loader.load()
    print(f"[1/4] Loaded {len(documents)} documents from {DOCS_PATH}")
    return documents


def split_documents(documents):
    """
    Split documents into chunks. The separator list respects our '## Question:'
    header structure first, so each Q&A pair stays intact as one chunk
    whenever possible, instead of being cut mid-answer.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    print(f"[2/4] Split into {len(chunks)} chunks")
    return chunks


def embed_and_store(chunks):
    """Embed chunks with a local HuggingFace model and persist to ChromaDB."""
    print("[3/4] Loading embedding model (sentence-transformers/all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("[4/4] Embedding chunks and writing to ChromaDB (this may take a minute)...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH,
        collection_name=COLLECTION_NAME,
    )
    print(f"Done. Vector DB persisted at: {os.path.abspath(DB_PATH)}")
    return vectorstore


def main():
    documents = load_documents()
    if not documents:
        raise RuntimeError(
            f"No .md files found in {DOCS_PATH}. Check the path and that your "
            "docs are actually .md files."
        )
    chunks = split_documents(documents)
    embed_and_store(chunks)
    print("\nIngestion complete. Your knowledge base is ready for retrieval.")


if __name__ == "__main__":
    main()