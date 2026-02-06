from typing import List

from sentence_transformers import SentenceTransformer

from .config import EMBEDDING_MODEL_NAME


class EmbeddingModel:
    """Wrapper around a sentence-transformers model."""

    def __init__(self, model_name: str | None = None) -> None:
        self.model_name = model_name or EMBEDDING_MODEL_NAME
        self._model = SentenceTransformer(self.model_name)

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Return embeddings for a list of texts."""
        embeddings = self._model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        return embeddings.tolist()

