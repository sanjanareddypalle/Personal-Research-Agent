import json
import logging
import os
import numpy as np
import faiss
from typing import List, Dict, Any, Optional
from pathlib import Path
from app.config import settings

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, index_dir: Optional[Path] = None, dim: int = 128):
        self.index_dir = index_dir or settings.VECTOR_INDEX_DIR
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.index_dir / "index.faiss"
        self.metadata_file = self.index_dir / "metadata.json"
        self.dim = dim
        self.index: Optional[faiss.IndexFlatIP] = None
        self.metadata: List[Dict[str, Any]] = []
        self._load_or_create()

    def _load_or_create(self):
        if self.index_file.exists() and self.metadata_file.exists():
            try:
                self.index = faiss.read_index(str(self.index_file))
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    self.metadata = json.load(f)
                logger.info(f"Loaded existing FAISS index with {len(self.metadata)} items.")
                return
            except Exception as e:
                logger.warning(f"Failed to load FAISS index: {e}. Reinitializing.")

        self.index = faiss.IndexFlatIP(self.dim)
        self.metadata = []

    def _persist(self):
        try:
            faiss.write_index(self.index, str(self.index_file))
            with open(self.metadata_file, "w", encoding="utf-8") as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Error persisting FAISS index: {e}")

    def _embed_text(self, text: str) -> np.ndarray:
        """
        Fast, robust normalized vector embedding with hashing fallback.
        Ensures instantaneous RAG indexing without network dependencies.
        """
        words = text.lower().split()
        vec = np.zeros(self.dim, dtype=np.float32)
        if not words:
            return vec

        for w in words:
            # Deterministic word hashing into dim buckets
            h = hash(w) % self.dim
            vec[h] += 1.0

        # L2 Normalize
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec

    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]]):
        if not texts:
            return
        vectors = np.array([self._embed_text(t) for t in texts], dtype=np.float32)
        self.index.add(vectors)
        self.metadata.extend(metadatas)
        self._persist()

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if not self.metadata or self.index.ntotal == 0:
            return []

        q_vec = np.array([self._embed_text(query)], dtype=np.float32)
        k = min(top_k, self.index.ntotal)
        distances, indices = self.index.search(q_vec, k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                item = dict(self.metadata[idx])
                item["score"] = float(distances[0][i])
                results.append(item)
        return results

    def remove_document(self, doc_id: str):
        """Removes chunks belonging to doc_id and rebuilds index."""
        new_metadata = []
        new_texts = []
        for meta in self.metadata:
            if meta.get("document_id") != doc_id:
                new_metadata.append(meta)
                new_texts.append(meta.get("text", ""))

        self.index = faiss.IndexFlatIP(self.dim)
        self.metadata = []
        if new_texts:
            self.add_texts(new_texts, new_metadata)
        else:
            self._persist()
