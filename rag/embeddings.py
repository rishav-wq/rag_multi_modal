from typing import List

from sentence_transformers import SentenceTransformer

from .config import EMBEDDING_MODEL_NAME


class EmbeddingModel:
    # Just a wrapper around sentence-transformers

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or EMBEDDING_MODEL_NAME
        self._model = SentenceTransformer(self.model_name)

    def embed(self, texts: List[str]) -> List[List[float]]:
        # Return embeddings for a list of texts
        # Note: could batch this better for large text lists
        embeddings = self._model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        # Could also use show_progress_bar=True for debugging
        return embeddings.tolist()

