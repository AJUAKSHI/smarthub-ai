import fitz  # PyMuPDF - reads PDFs
import chromadb
from sentence_transformers import SentenceTransformer
from docx import Document
import os

# Setup ChromaDB - persistent storage
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="smarthub_docs")

# Setup embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_from_pdf(file_path: str) -> str:
    """Read all text from a PDF file"""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file_path: str) -> str:
    """Read all text from a DOCX file"""
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_txt(file_path: str) -> str:
    """Read all text from a TXT file"""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return text


def get_document_text(filename: str) -> str:
    """
    Retrieve all chunks belonging to a document.
    """
    results = collection.get(
        where={"filename": filename}
    )

    documents = results.get("documents", [])

    return "\n".join(documents)





def extract_text(file_path: str, filename: str) -> str:
    """Decide which extractor to use based on file type"""
    extension = filename.split(".")[-1].lower()
    
    if extension == "pdf":
        return extract_text_from_pdf(file_path)
    elif extension == "docx":
        return extract_text_from_docx(file_path)
    elif extension == "txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {extension}. Only PDF, DOCX, TXT allowed.")

def chunk_text(text: str, chunk_size: int = 500) -> list:
    """Split text into smaller chunks"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def ingest_document(file_path: str, filename: str) -> dict:
    """Process a document and store it in ChromaDB"""
    # Step 1: Extract text based on file type
    text = extract_text(file_path, filename)
    
    # Step 2: Split into chunks
    chunks = chunk_text(text)
    
    # Step 3: Create embeddings and store
    for i, chunk in enumerate(chunks):
        embedding = embedding_model.encode(chunk).tolist()
        collection.add(
    documents=[chunk],
    embeddings=[embedding],
    ids=[f"{filename}_chunk_{i}"],
    metadatas=[
        {
            "filename": filename
        }
    ]
)
    
    return {"filename": filename, "chunks_stored": len(chunks)}

def query_documents(question: str) -> str:
    """Search ChromaDB for relevant chunks"""
    question_embedding = embedding_model.encode(question).tolist()
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )
    
    chunks = results["documents"][0]
    return "\n\n".join(chunks)