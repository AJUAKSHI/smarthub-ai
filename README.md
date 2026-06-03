# SmartHub AI/LLM Module
**G4 Delta — AI/LLM Role | CIXIO TKM Internship 2026**

## What This Does
AI-powered backend service for SmartHub with:
- AI Chat with conversation history
- RAG Pipeline — upload documents and ask questions about them
- Document Summarization
- Supports PDF, DOCX, TXT files

## Tech Stack
- Python + FastAPI
- Groq API (LLaMA 3.3 70B)
- ChromaDB (Vector Database)
- Sentence Transformers (Embeddings)

## How to Run
1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install packages: `pip install -r requirements.txt`
5. Create `.env` file and add: `GROQ_API_KEY=your_key_here`
6. Run: `uvicorn main:app --reload`
7. Open: `http://localhost:8000/docs`

## API Endpoints
- `POST /chat` — AI chat with history
- `POST /rag/ingest` — Upload PDF/DOCX/TXT
- `POST /rag/query` — Ask questions about documents
- `POST /rag/summarize` — Summarize uploaded document