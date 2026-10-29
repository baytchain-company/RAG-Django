import requests

from .base import Embedder


class OllamaEmbedder(Embedder):
    """Local embeddings via Ollama, e.g. `ollama pull nomic-embed-text` (768 dims)."""

    def __init__(self, model: str, dim: int, url: str):
        self.model, self.dim, self.url = model, dim, url.rstrip("/")

    def _embed(self, texts):
        r = requests.post(f"{self.url}/api/embed", json={"model": self.model, "input": texts}, timeout=120)
        r.raise_for_status()
        return self._check(r.json()["embeddings"])

    def embed_documents(self, texts):
        return self._embed(texts)

    def embed_query(self, text):
        return self._embed([text])[0]
