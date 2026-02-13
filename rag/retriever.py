from __future__ import annotations

from typing import Any, Dict, List

from .embeddings import EmbeddingModel
from .vector_store import FaissVectorStore


class Retriever:
    # Semantic retriever using FAISS vector store

    def __init__(self, top_k: int = 5) -> None:
        self.top_k = top_k  # TODO: make this configurable from API?
        self.embedder = EmbeddingModel()
        self.store = FaissVectorStore()
        self._loaded = False  # lazy-load index on first use

    def _ensure_loaded(self) -> None:
        if not self._loaded:
            self.store.load()
            self._loaded = True

    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        self._ensure_loaded()
        q_emb = self.embedder.embed([query])[0]
        results = self.store.search(q_emb, top_k=self.top_k)
        
        # build context list
        contexts = []
        for meta, score in results:
            contexts.append({
                "score": score,
                "source": meta.get("source"),
                "chunk_id": meta.get("chunk_id"),
                "doc_id": meta.get("doc_id"),
                "text": meta.get("text"),
            })
        return contexts

