import requests

from .base import Embedder


class OpenAIEmbedder(Embedder):
    """Any OpenAI-compatible /embeddings endpoint (OpenAI: text-embedding-3-small = 1536 dims)."""

    def __init__(self, model: str, dim: int, base_url: str, api_key: str):
        self.model, self.dim = model, dim
        self.base_url, self.api_key = base_url.rstrip("/"), api_key

    def _embed(self, texts):
        r = requests.post(
            f"{self.base_url}/embeddings",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": self.model, "input": texts},
            timeout=120,
        )
        r.raise_for_status()
        data = sorted(r.json()["data"], key=lambda d: d["index"])
        return self._check([d["embedding"] for d in data])

    def embed_documents(self, texts):
        return self._embed(texts)

    def embed_query(self, text):
        return self._embed([text])[0]
