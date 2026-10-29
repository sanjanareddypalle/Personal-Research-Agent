import uuid
import logging
import os
from typing import List, Dict, Any, Optional
from app.retrieval.parser import extract_text_from_file, chunk_text
from app.retrieval.vector_store import VectorStore
from app.schemas.document import DocumentChunk

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.vector_store = VectorStore()

    def process_and_index_document(self, doc_id: str, file_path: str, filename: str) -> int:
        """Parses a document file, chunks it, and indexes it into the vector store."""
        pages = extract_text_from_file(file_path)
        all_chunks = []
        all_metas = []

        for p in pages:
            page_text = p["text"]
            page_num = p["page_number"]
            chunks = chunk_text(page_text, chunk_size=500, overlap=100)
            for idx, c in enumerate(chunks):
                chunk_id = f"{doc_id}_{len(all_chunks)}"
                all_chunks.append(c)
                all_metas.append({
                    "id": chunk_id,
                    "document_id": doc_id,
                    "document_name": filename,
                    "page_number": page_num,
                    "chunk_index": idx,
                    "text": c
                })

        if all_chunks:
            self.vector_store.add_texts(all_chunks, all_metas)
            logger.info(f"Indexed {len(all_chunks)} chunks for document {filename} ({doc_id})")

        return len(all_chunks)

    def search_knowledge(self, query: str, top_k: int = 5) -> List[DocumentChunk]:
        raw_results = self.vector_store.search(query, top_k=top_k)
        chunks = []
        for r in raw_results:
            chunks.append(DocumentChunk(
                id=r.get("id", str(uuid.uuid4())),
                document_id=r.get("document_id", ""),
                document_name=r.get("document_name", "Unknown"),
                page_number=r.get("page_number"),
                chunk_index=r.get("chunk_index", 0),
                text=r.get("text", ""),
                score=r.get("score")
            ))
        return chunks

    def remove_document(self, doc_id: str):
        self.vector_store.remove_document(doc_id)

rag_service = RAGService()
