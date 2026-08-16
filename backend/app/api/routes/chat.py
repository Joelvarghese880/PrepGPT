"""
POST /chat endpoint. Takes a question + session_id, returns a grounded
answer + sources, using per-session conversational memory.
"""

from fastapi import APIRouter, HTTPException

from app.models.schemas import ChatRequest, ChatResponse
from app.core.rag_chain import build_rag_chain_with_memory

router = APIRouter()

# Built once at import time, not per-request — see note in main.py.
_chain = build_rag_chain_with_memory()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        result = _chain.invoke(
            {"question": request.question},
            config={"configurable": {"session_id": request.session_id}},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chain error: {str(e)}")

    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"],
    )