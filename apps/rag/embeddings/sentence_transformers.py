from .base import Embedder


class SentenceTransformersEmbedder(Embedder):
    """Free, runs on your machine. Default: intfloat/multilingual-e5-small (384 dims, ~100 languages incl. Uzbek)."""

    def __init__(self, model: str, dim: int):
        from sentence_transformers import SentenceTransformer  # heavy import, load lazily

        self.model = SentenceTransformer(model)
        self.dim = dim
        # e5 models expect "query: " / "passage: " prefixes
        self._e5 = "e5" in model.lower()

    def _encode(self, texts):
        return self.model.encode(texts, normalize_embeddings=True, batch_size=32).tolist()

    def embed_documents(self, texts):
        prefix = "passage: " if self._e5 else ""
        return self._check(self._encode([prefix + t for t in texts]))

    def embed_query(self, text):
        prefix = "query: " if self._e5 else ""
        return self._check(self._encode([prefix + text]))[0]
