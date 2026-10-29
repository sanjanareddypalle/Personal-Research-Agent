import pytest
import tempfile
import os
from pathlib import Path
from app.retrieval.parser import chunk_text, extract_text_from_file
from app.retrieval.vector_store import VectorStore
from app.retrieval.rag_service import RAGService

def test_chunking_with_overlap():
    text = "word " * 200  # 1000 chars
    chunks = chunk_text(text, chunk_size=300, overlap=50)
    assert len(chunks) > 1
    # Verify overlap exists between chunk 0 and 1
    assert chunks[0][-50:] == chunks[1][:50]

def test_txt_extraction():
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as f:
        f.write("Line 1\nLine 2\nLine 3")
        f_path = f.name
    try:
        pages = extract_text_from_file(f_path)
        assert len(pages) == 1
        assert "Line 2" in pages[0]["text"]
    finally:
        os.remove(f_path)

def test_vector_store_indexing_and_search():
    with tempfile.TemporaryDirectory() as tmpdir:
        vs = VectorStore(index_dir=Path(tmpdir))
        texts = [
            "LangGraph enables stateful multi-agent cycles and persistent checkpoints.",
            "FastAPI provides high performance asynchronous web APIs in Python.",
            "Kubernetes orchestrates containerized services in distributed clouds."
        ]
        metadatas = [
            {"id": "c1", "document_id": "doc1", "document_name": "langgraph.md", "text": texts[0]},
            {"id": "c2", "document_id": "doc2", "document_name": "fastapi.md", "text": texts[1]},
            {"id": "c3", "document_id": "doc3", "document_name": "k8s.md", "text": texts[2]}
        ]
        vs.add_texts(texts, metadatas)
        assert vs.index.ntotal == 3

        # Search for agent multi-agent
        results = vs.search("multi-agent cycles", top_k=2)
        assert len(results) > 0
        assert results[0]["document_name"] == "langgraph.md"

        # Remove doc1
        vs.remove_document("doc1")
        assert vs.index.ntotal == 2
