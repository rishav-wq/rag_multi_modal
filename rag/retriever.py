from __future__ import annotations

from typing import Any, Dict, List

from .embeddings import EmbeddingModel
from .vector_store import FaissVectorStore


class Retriever:
    """Semantic retriever over the FAISS vector store."""

    def __init__(self, top_k: int = 5) -> None:
        self.top_k = top_k
        self.embedder = EmbeddingModel()
        self.store = FaissVectorStore()
        # Lazy-load index on first use
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if not self._loaded:
            self.store.load()
            self._loaded = True

    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        self._ensure_loaded()
        q_emb = self.embedder.embed([query])[0]
        results = self.store.search(q_emb, top_k=self.top_k)
        contexts: List[Dict[str, Any]] = []
        for meta, score in results:
            contexts.append(
                {
                    "score": score,
                    "source": meta.get("source"),
                    "chunk_id": meta.get("chunk_id"),
                    "doc_id": meta.get("doc_id"),
                    "text": meta.get("text"),
                }
            )
        return contexts

