"""
PrepGPT backend entrypoint.

Run (from the backend/ folder):
    uvicorn app.main:app --reload

Docs available at:
    http://127.0.0.1:8000/docs
"""

import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"  # must be set before chromadb import

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import chat

app = FastAPI(
    title="PrepGPT API",
    description="RAG-powered interview prep chatbot for DSA, OOP, SQL, DBMS, OS, and CN.",
    version="0.1.0",
)

# CORS: allows your React frontend (running on a different port, e.g. 5173)
# to make requests to this API. Without this, the browser blocks the requests.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server default
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api", tags=["chat"])


@app.get("/")
def root():
    return {"status": "PrepGPT API is running", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}