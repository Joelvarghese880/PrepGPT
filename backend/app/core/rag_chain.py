"""
Phase 3 + Phase 5: The RAG chain, now with conversational memory.

Flow per request:
    1. Take the raw question + chat history for this session
    2. LLM rewrites the question into a standalone version using history
       (so "what's its time complexity?" becomes a real, retrievable question)
    3. Retriever fetches chunks using the REWRITTEN question
    4. Answer is generated using retrieved context + original conversation
    5. Both question and answer are saved back into session history
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq import ChatGroq

from app.config import settings
from app.core.vectorstore import get_retriever
from app.core.memory import get_session_history


SYSTEM_PROMPT = """You are PrepGPT, an interview preparation assistant for a software \
engineering fresher. You answer questions about DSA, OOP, SQL, DBMS, OS, and \
Computer Networks using ONLY the context provided below.

Rules:
- Answer clearly and concisely, the way you'd explain it out loud in an interview.
- If the context doesn't contain the answer, say so honestly instead of guessing \
or using outside knowledge.
- When relevant, mention time/space complexity or give a short code snippet.
- Do not mention "the context" or "the documents" in your answer — just answer \
naturally as if you know this material.

Context:
{context}
"""

# Used to rewrite a follow-up question into a standalone one, using history.
CONDENSE_QUESTION_PROMPT = """Given the conversation history and a follow-up question, \
rewrite the follow-up question as a standalone question that makes sense without \
the history. If the question is already standalone, return it unchanged. \
Return ONLY the rewritten question, nothing else."""


def format_docs(docs) -> str:
    return "\n\n---\n\n".join(
        f"[Source: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
        for doc in docs
    )


def build_rag_chain_with_memory():
    """
    Returns a RunnableWithMessageHistory that expects invoke() calls like:

        chain.invoke(
            {"question": "..."},
            config={"configurable": {"session_id": "some-session-id"}},
        )

    and returns: {"answer": str, "sources": list[dict]}
    """
    retriever = get_retriever(k=4)

    llm = ChatGroq(
        model=settings.groq_model,
        api_key=settings.groq_api_key,
        temperature=0.2,
    )

    condense_prompt = ChatPromptTemplate.from_messages([
        ("system", CONDENSE_QUESTION_PROMPT),
        MessagesPlaceholder("chat_history"),
        ("human", "{question}"),
    ])
    condense_chain = condense_prompt | llm | StrOutputParser()

    answer_prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("chat_history"),
        ("human", "{question}"),
    ])

    def full_chain(input_dict: dict, config=None) -> dict:
        question = input_dict["question"]
        chat_history = input_dict.get("chat_history", [])

        # Step 1: rewrite question to be standalone if there's history
        if chat_history:
            standalone_question = condense_chain.invoke({
                "question": question,
                "chat_history": chat_history,
            })
        else:
            standalone_question = question

        # Step 2: retrieve using the standalone question
        docs = retriever.invoke(standalone_question)
        context = format_docs(docs)

        # Step 3: generate the answer using original question + history + context
        answer = (answer_prompt | llm | StrOutputParser()).invoke({
            "question": question,
            "chat_history": chat_history,
            "context": context,
        })

        sources = list({
            d.metadata.get("source", "unknown"): {
                "source": d.metadata.get("source", "unknown"),
                "preview": d.page_content[:150],
            }
            for d in docs
        }.values())

        return {"answer": answer, "sources": sources}

    chain_with_history = RunnableWithMessageHistory(
        RunnableLambda(full_chain),
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
    return chain_with_history