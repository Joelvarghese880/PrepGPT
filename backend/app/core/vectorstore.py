"""
Loads the already-built ChromaDB vector store (from Phase 2's ingest.py)
and exposes a retriever for the RAG chain.

This module does NOT re-embed anything — it just connects to the
persisted store on disk.
"""

import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from app.config import settings


def get_vectorstore() -> Chroma:
    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
    return Chroma(
        persist_directory=settings.chroma_db_path,
        embedding_function=embeddings,
        collection_name=settings.chroma_collection_name,
    )


def get_retriever(k: int = 4):
    """
    k = how many chunks to retrieve per query.
    4 is a reasonable default: enough context for a good answer,
    not so much that the LLM prompt gets bloated or noisy.
    """
    vectorstore = get_vectorstore()
    return vectorstore.as_retriever(search_kwargs={"k": k})