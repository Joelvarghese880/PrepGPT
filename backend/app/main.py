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
from app.config import settings

app = FastAPI(
    title="PrepGPT API",
    description="RAG-powered interview prep chatbot for DSA, OOP, SQL, DBMS, OS, and CN.",
    version="0.1.0",
)

# CORS: allows your React frontend to make requests to this API.
# Origins are read from ALLOWED_ORIGINS env var (comma-separated) —
# update this in Render's dashboard once you have your Vercel URL,
# no code change needed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
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