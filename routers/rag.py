from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from services.rag_service import ingest_document, query_documents
from services.ai_service import get_ai_response
import os
import shutil


from services.ai_service import summarize_text
from services.rag_service import get_document_text


from services.rag_service import collection


router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed file types
ALLOWED_EXTENSIONS = ["pdf", "docx", "txt"]

class QueryRequest(BaseModel):
    question: str

@router.post("/rag/ingest")
def ingest(file: UploadFile = File(...)):
    # Check file type first
    extension = file.filename.split(".")[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{extension}' not supported. Only PDF, DOCX, TXT allowed."
        )
    
    # Save the uploaded file
    file_path = f"{UPLOAD_FOLDER}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process and store in ChromaDB
    try:
        result = ingest_document(file_path, file.filename)
        return {
            "message": "Document uploaded and processed successfully!",
            "filename": result["filename"],
            "chunks_stored": result["chunks_stored"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/rag/query")
def query(request: QueryRequest):
    try:
        # Search ChromaDB for relevant chunks
        relevant_chunks = query_documents(request.question)
        
        # Build prompt with context
        prompt = f"""You are SmartHub AI. Answer the question using the context below.
        
Context from uploaded documents:
{relevant_chunks}

Question: {request.question}

Answer:"""
        
        reply = get_ai_response(prompt)
        return {
            "question": request.question,
            "answer": reply,
            "source": "SmartHub RAG Pipeline"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    





class SummaryRequest(BaseModel):
    filename: str

@router.post("/rag/summarize")
def summarize(request: SummaryRequest):

    text = get_document_text(request.filename)

    if not text:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    summary = summarize_text(text)

    return {
        "filename": request.filename,
        "summary": summary
    }

