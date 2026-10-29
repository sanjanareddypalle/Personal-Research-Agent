from typing import List, Optional
from pydantic import BaseModel, Field

class DocumentResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    file_size_bytes: int
    chunk_count: int
    created_at: str

class DocumentChunk(BaseModel):
    id: str
    document_id: str
    document_name: str
    page_number: Optional[int] = None
    chunk_index: int
    text: str
    score: Optional[float] = None

class KnowledgeSearchRequest(BaseModel):
    query: str
    top_k: int = Field(5, ge=1, le=20)

class KnowledgeSearchResponse(BaseModel):
    query: str
    chunks: List[DocumentChunk]
