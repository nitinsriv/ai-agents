MVP AI RAG Chat

This is a minimal MVP that loads PDFs from `backend/pdfs`, embeds their text using OpenAI embeddings, stores them in-memory, and provides a `/api/chat` endpoint that answers questions using retrieved document snippets (RAG).

Quick start (Python)

1. Copy your PDFs into `backend/pdfs` (create the folders if missing).
2. Create a `.env` file (or set `OPENAI_API_KEY` in your environment).
3. Install dependencies and run the FastAPI server:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn server.app:app --reload --port 8000
```

Open http://localhost:8000 in your browser.

Notes
- This MVP uses an in-memory vector store — restart clears the index.
- For production, use a persistent vector DB (e.g., Pinecone, Weaviate) and robust chunking.
- The `server/rag.py` file demonstrates embedding + retrieval + LLM answer composition using OpenAI.

Documentation
- Project plan: [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md)
- Architecture: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- API spec: [docs/API_SPEC.md](docs/API_SPEC.md)
- Wireframe: [docs/WIREFRAME.md](docs/WIREFRAME.md)
