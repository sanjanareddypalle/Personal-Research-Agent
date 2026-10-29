import os
from typing import List, Dict, Any
from pypdf import PdfReader

def extract_text_from_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Extracts text and page numbers from PDF, Markdown, and TXT files.
    Returns a list of dicts: [{"text": str, "page_number": int | None}]
    """
    ext = os.path.splitext(file_path)[1].lower()
    pages_data = []

    if ext == ".pdf":
        try:
            reader = PdfReader(file_path)
            for idx, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                if text.strip():
                    pages_data.append({"text": text.strip(), "page_number": idx + 1})
        except Exception as e:
            pages_data.append({"text": f"Error reading PDF: {e}", "page_number": 1})
    elif ext in [".txt", ".md", ".markdown"]:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if content.strip():
                    pages_data.append({"text": content.strip(), "page_number": None})
        except Exception as e:
            pages_data.append({"text": f"Error reading file: {e}", "page_number": None})
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    return pages_data

def chunk_text(text: str, chunk_size: int = 600, overlap: int = 100) -> List[str]:
    """Splits text into chunks with sliding window overlap."""
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
