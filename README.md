# PrepGPT 🎓

**A retrieval-augmented (RAG) chatbot that answers software engineering interview questions — grounded in a real knowledge base, not hallucinated.**

🔗 **Live demo:** [prep-gpt-five.vercel.app](https://prep-gpt-five.vercel.app/)
🔗 **Backend API docs:** [prepgpt-backend-79m5.onrender.com/docs](https://prepgpt-backend-79m5.onrender.com/docs)

> Note: the backend is hosted on Render's free tier, which sleeps after 15 minutes of inactivity. The first request after idle time may take 30-50 seconds to respond while it wakes up.

---

## What it does

PrepGPT answers interview-prep questions across **DSA, OOP, SQL, DBMS, Operating Systems, and Computer Networks** — but instead of relying purely on an LLM's training data, it retrieves relevant content from a curated knowledge base first, then generates an answer grounded in that retrieved context. Every answer shows exactly which source document it was grounded in.

It also maintains **conversational memory per session**, so follow-up questions like *"what's its time complexity?"* correctly resolve to whatever was just discussed.

## Why RAG instead of just calling an LLM?

A raw LLM call can hallucinate plausible-sounding but wrong technical details, and can't cite where an answer came from. RAG (Retrieval-Augmented Generation) fixes this by:
1. Retrieving the most relevant chunks from a real knowledge base using semantic search
2. Feeding those chunks to the LLM as context
3. Instructing the model to answer *only* from that context

This makes answers verifiable and reduces hallucination — critical for something people might actually study from.

## Architecture

```
┌─────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   React UI   │ ─────▶  │   FastAPI Backend  │ ─────▶  │  ChromaDB (vector) │
│  (Vercel)   │  HTTP   │     (Render)      │         │   store          │
└─────────────┘         └──────────────────┘         └─────────────────┘
                                  │                             ▲
                                  │                             │
                                  ▼                             │
                          ┌──────────────┐             ┌───────────────┐
                          │  Groq LLM    │             │  Ingestion    │
                          │ (generation) │             │  Pipeline     │
                          └──────────────┘             │  (fastembed)  │
                                                        └───────────────┘
                                                                ▲
                                                                │
                                                        interview_prep_docs/
                                                        (DSA, OOP, SQL, DBMS,
                                                         OS, CN — markdown)
```

**Flow per question:**
1. If there's conversation history, the LLM rewrites the question into a standalone version (so follow-ups work)
2. The standalone question is embedded and used to semantically search ChromaDB for the most relevant chunks
3. Retrieved chunks + conversation history + the question are sent to Groq's LLM
4. The answer is generated, grounded in retrieved context, and returned with source attribution

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, plain CSS (custom design system) |
| Backend | FastAPI, Python 3.12 |
| LLM orchestration | LangChain (LCEL, RunnableWithMessageHistory) |
| LLM | Groq (`openai/gpt-oss-120b`) |
| Vector store | ChromaDB |
| Embeddings | fastembed (ONNX-based, `BAAI/bge-small-en-v1.5`) |
| Deployment | Render (backend), Vercel (frontend) |

## Key engineering decisions

- **Header-aware chunking** — the knowledge base docs use consistent `## Question:` headers, and the text splitter respects these boundaries first, so Q&A pairs stay intact instead of being cut mid-answer.
- **Session-based memory without a database** — uses an in-memory store keyed by session ID for simplicity in this deployment; documented as a known limitation (would swap for Redis/Postgres for multi-instance production use).
- **Switched from `sentence-transformers`/PyTorch to `fastembed` (ONNX)** for embeddings after hitting a 512MB out-of-memory crash on Render's free tier — PyTorch's runtime footprint alone exceeded the limit. This cut memory usage significantly with no quality loss.
- **Configurable CORS via environment variable** rather than hardcoded origins, so the allowed frontend URL can change per environment without a code change.

## Running locally

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

cp .env.example .env
# then edit .env and add your GROQ_API_KEY (free at console.groq.com/keys)

python -m app.ingestion.ingest      # builds the vector store
python -m uvicorn app.main:app --reload
```
API docs available at `http://127.0.0.1:8000/docs`

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
Runs at `http://localhost:5173`

## Project structure

```
prepGPT/
├── backend/
│   ├── app/
│   │   ├── ingestion/      # doc loading, chunking, embedding pipeline
│   │   ├── core/           # RAG chain, vector store, session memory
│   │   ├── api/routes/     # FastAPI endpoints
│   │   └── models/         # Pydantic schemas
│   └── interview_prep_docs/  # the knowledge base (markdown)
└── frontend/
    └── src/
        ├── components/     # chat UI
        ├── hooks/          # chat state management
        └── api/            # backend client
```

## What's next

- Swap in-memory session store for a persistent one (Redis) to survive server restarts
- Add topic-filtered retrieval (metadata filtering by subject)
- Expand the knowledge base with more DSA problems and system design content

---

Built as a portfolio project to explore practical RAG system design — from chunking strategy through production deployment debugging (Python version pinning, memory-constrained embedding model selection, cross-platform case-sensitivity issues).