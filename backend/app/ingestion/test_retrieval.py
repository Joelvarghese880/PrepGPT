"""
Quick sanity check for Phase 2: confirms ChromaDB retrieval actually works
before we build the full RAG chain around it.

Usage (from the backend/ folder):
    python -m app.ingestion.test_retrieval
"""

import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"  # silence ChromaDB telemetry noise

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DB_PATH = "./chroma_db"
COLLECTION_NAME = "interview_prep"

TEST_QUERIES = [
    "How do I detect a cycle in a linked list?",
    "What is the difference between primary key and foreign key?",
    "Explain polymorphism in Python OOP",
]


def main():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
    )

    print(f"Loaded collection '{COLLECTION_NAME}' with "
          f"{vectorstore._collection.count()} chunks.\n")

    for query in TEST_QUERIES:
        print(f"QUERY: {query}")
        results = vectorstore.similarity_search(query, k=2)
        for i, doc in enumerate(results, 1):
            source = doc.metadata.get("source", "unknown")
            preview = doc.page_content[:150].replace("\n", " ")
            print(f"  [{i}] source={source}")
            print(f"      {preview}...")
        print()


if __name__ == "__main__":
    main()