from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from .config import DATA_DIR, ensure_data_dir
from .embeddings import EmbeddingModel
from .vector_store import FaissVectorStore


def load_text_from_file(path: Path) -> str:
    # Support .txt and .md files for now
    # could add PDF support later if needed
    if path.suffix.lower() in [".txt", ".md"]:
        return path.read_text(encoding="utf-8", errors="ignore")
    raise ValueError(f"Unsupported file type: {path.suffix}. Supported: .txt, .md")


def simple_chunk_text(text: str, max_chars: int = 800, overlap: int = 200) -> List[str]:
    # Naive chunking by character count with overlap
    # TODO: could use smarter chunking like by sentences or paragraphs
    # maybe try langchain's text splitter later?
    chunks: List[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + max_chars, n)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += max_chars - overlap
    return chunks


def ingest_documents():
    # Load documents from DATA_DIR, chunk them, embed, and build FAISS index
    ensure_data_dir()
    # Get all files and filter for supported extensions (.txt, .md)
    files = sorted(
        p for p in DATA_DIR.iterdir() 
        if p.is_file() and p.suffix.lower() in [".txt", ".md"]
    )
    if not files:
        raise RuntimeError(f"No .txt or .md files found in {DATA_DIR}. Place your documents there.")

    print(f"Found {len(files)} documents to process")
    all_chunks: List[str] = []
    metadatas: List[Dict] = []

    for doc_id, path in enumerate(files):
        text = load_text_from_file(path)
        chunks = simple_chunk_text(text)
        # chunks = simple_chunk_text(text, max_chars=1000)  # can adjust size
        print(f"  {path.name}: {len(chunks)} chunks")
        for chunk_id, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            metadatas.append(
                {
                    "doc_id": doc_id,
                    "source": path.name,
                    "chunk_id": chunk_id,
                    "text": chunk,
                }
            )

    print(f"Total chunks: {len(all_chunks)}")
    print("Generating embeddings...")
    embedder = EmbeddingModel()
    embeddings = embedder.embed(all_chunks)

    print("Building FAISS index...")
    store = FaissVectorStore()
    store.build(embeddings, metadatas)
    print("Done!")


if __name__ == "__main__":
    ingest_documents()

