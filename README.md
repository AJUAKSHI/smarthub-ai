# SmartHub AI/LLM Module
**G4 Delta — AI/LLM Role | CIXIO TKM Internship 2026**

## What This Does
AI-powered backend service for SmartHub with:
- AI Chat with conversation history
- RAG Pipeline — upload documents and ask questions about them
- Document Summarization
- Multi-format support: PDF, DOCX, TXT, PNG, JPG (with OCR)
- Document management — list and delete uploaded files

## Tech Stack
- Python + FastAPI
- Groq API (LLaMA 3.3 70B)
- ChromaDB (Vector Database)
- Sentence Transformers (Embeddings)
- Pytesseract + Pillow (OCR for images)
- PyMuPDF (PDF extraction)
- python-docx (DOCX extraction)

## How to Run
1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install packages: `pip install -r requirements.txt`
5. Install Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki
6. Create `.env` file and add: `GROQ_API_KEY=your_key_here`
7. Run: `uvicorn main:app --reload`
8. Open: `http://localhost:8000/docs`

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /chat | AI chat with conversation history |
| POST | /rag/ingest | Upload PDF, DOCX, TXT, PNG, JPG |
| POST | /rag/query | Ask questions about uploaded documents |
| POST | /rag/summarize | Summarize an uploaded document |
| GET | /rag/documents | List all uploaded documents |
| DELETE | /rag/documents/{filename} | Delete a specific document |