from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import faiss
import numpy as np

from .config import FAISS_INDEX_PATH, METADATA_PATH


class FaissVectorStore:
    # FAISS-based vector store with JSON metadata

    def __init__(
        self,
        index_path: Path | None = None,
        metadata_path: Path | None = None,
    ) -> None:
        self.index_path = index_path or FAISS_INDEX_PATH
        self.metadata_path = metadata_path or METADATA_PATH
        self.index: faiss.Index | None = None
        self.metadata: List[Dict[str, Any]] = []

    def _ensure_dim(self, dim: int) -> None:
        if self.index is None:
            # Use inner product index; normalize embeddings before add/search
            # could also try IndexFlatL2 but IP works better with normalized vecs
            self.index = faiss.IndexFlatIP(dim)

    def build(self, embeddings: List[List[float]], metadatas: List[Dict[str, Any]]) -> None:
        if len(embeddings) == 0:
            raise ValueError("No embeddings to build index.")

        # convert to numpy array and normalize for cosine similarity
        x = np.array(embeddings, dtype="float32")
        faiss.normalize_L2(x)  # important for IndexFlatIP to work as cosine
        self._ensure_dim(x.shape[1])
        self.index.add(x)
        self.metadata = metadatas
        self.save()

    def save(self) -> None:
        if self.index is None:
            raise ValueError("Index is not initialized.")
        faiss.write_index(self.index, str(self.index_path))
        with self.metadata_path.open("w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    def load(self) -> None:
        if not self.index_path.exists() or not self.metadata_path.exists():
            raise FileNotFoundError("Index or metadata not found; please run ingestion first.")
        self.index = faiss.read_index(str(self.index_path))
        with self.metadata_path.open("r", encoding="utf-8") as f:
            self.metadata = json.load(f)

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
    ) -> List[Tuple[Dict[str, Any], float]]:
        if self.index is None:
            self.load()

        xq = np.array([query_embedding], dtype="float32")
        faiss.normalize_L2(xq)  # normalize query vector
        scores, indices = self.index.search(xq, top_k)
        
        results: List[Tuple[Dict[str, Any], float]] = []
        for idx, score in zip(indices[0], scores[0]):
            if idx == -1:  # faiss returns -1 for missing results
                continue
            meta = self.metadata[int(idx)]
            results.append((meta, float(score)))
        return results

