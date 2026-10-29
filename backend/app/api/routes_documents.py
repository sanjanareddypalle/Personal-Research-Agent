import os
import uuid
import shutil
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config import settings
from app.database.session import SyncSessionLocal
from app.database.repository import DocumentRepository
from app.schemas.document import DocumentResponse, KnowledgeSearchRequest, KnowledgeSearchResponse
from app.retrieval.rag_service import rag_service

router = APIRouter(prefix="/documents", tags=["Knowledge Base & RAG"])

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """Uploads PDF, TXT, or Markdown document and indexes chunks into FAISS."""
    filename = file.filename or "uploaded_file"
    ext = os.path.splitext(filename)[1].lower()
    if ext not in [".pdf", ".txt", ".md", ".markdown"]:
        raise HTTPException(status_code=400, detail="Only PDF, TXT, and Markdown files are supported.")

    doc_id = str(uuid.uuid4())
    saved_path = settings.UPLOAD_DIR / f"{doc_id}_{filename}"

    with open(saved_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    file_size = os.path.getsize(saved_path)

    # Process and index chunks
    chunk_count = rag_service.process_and_index_document(doc_id, str(saved_path), filename)

    # Record in DB
    with SyncSessionLocal() as session:
        repo = DocumentRepository(session)
        doc = repo.add_document(
            doc_id=doc_id,
            filename=filename,
            file_type=ext.replace(".", ""),
            file_size=file_size,
            chunk_count=chunk_count,
            file_path=str(saved_path)
        )
        return DocumentResponse(
            id=doc.id,
            filename=doc.filename,
            file_type=doc.file_type,
            file_size_bytes=doc.file_size_bytes,
            chunk_count=doc.chunk_count,
            created_at=doc.created_at.strftime("%Y-%m-%d %H:%M")
        )

@router.get("", response_model=List[DocumentResponse])
def list_documents():
    with SyncSessionLocal() as session:
        repo = DocumentRepository(session)
        docs = repo.list_documents()
        return [
            DocumentResponse(
                id=d.id,
                filename=d.filename,
                file_type=d.file_type,
                file_size_bytes=d.file_size_bytes,
                chunk_count=d.chunk_count,
                created_at=d.created_at.strftime("%Y-%m-%d %H:%M")
            ) for d in docs
        ]

@router.delete("/{document_id}")
def delete_document(document_id: str):
    with SyncSessionLocal() as session:
        repo = DocumentRepository(session)
        doc = repo.get_document(document_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Remove from disk and vector index
        if os.path.exists(doc.file_path):
            try:
                os.remove(doc.file_path)
            except Exception:
                pass
        rag_service.remove_document(document_id)
        repo.delete_document(document_id)
        return {"status": "success", "message": f"Document {document_id} removed."}

@router.post("/search", response_model=KnowledgeSearchResponse)
def search_knowledge(req: KnowledgeSearchRequest):
    chunks = rag_service.search_knowledge(req.query, top_k=req.top_k)
    return KnowledgeSearchResponse(query=req.query, chunks=chunks)
