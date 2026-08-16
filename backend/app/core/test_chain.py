"""
Phase 5 sanity check: confirms conversational memory works — ask a question,
then a follow-up that only makes sense with history ("what about its
complexity?"), and see if the retriever + answer stay on-topic.

Usage (from the backend/ folder):
    python -m app.core.test_chain
"""

import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"  # must be set before chromadb import

from app.core.rag_chain import build_rag_chain_with_memory

SESSION_ID = "terminal-test-session"


def main():
    chain = build_rag_chain_with_memory()

    print("PrepGPT terminal test (with memory). Type a question, or 'quit' to exit.\n")
    while True:
        question = input("You: ").strip()
        if question.lower() in {"quit", "exit"}:
            break
        if not question:
            continue

        result = chain.invoke(
            {"question": question},
            config={"configurable": {"session_id": SESSION_ID}},
        )

        print(f"\nPrepGPT: {result['answer']}\n")
        print("Sources used:")
        for s in result["sources"]:
            print(f"  - {s['source']}")
        print()


if __name__ == "__main__":
    main()