"""Offline embedder for tests and quick demos. No model download, no meaning — only word overlap."""
import hashlib
import math
import re

from .base import Embedder

_WORD = re.compile(r"\w+", re.UNICODE)


class HashingEmbedder(Embedder):
    def __init__(self, dim: int):
        self.dim = dim

    def _vec(self, text: str) -> list[float]:
        v = [0.0] * self.dim
        words = _WORD.findall(text.lower())
        features = words + [w[i : i + 4] for w in words for i in range(max(1, len(w) - 3))]
        for f in features:
            h = int(hashlib.md5(f.encode()).hexdigest(), 16)
            v[h % self.dim] += 1.0 if (h >> 8) & 1 else -1.0
        norm = math.sqrt(sum(x * x for x in v)) or 1.0
        return [x / norm for x in v]

    def embed_documents(self, texts):
        return [self._vec(t) for t in texts]

    def embed_query(self, text):
        return self._vec(text)
