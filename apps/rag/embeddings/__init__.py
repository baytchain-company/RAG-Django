from functools import lru_cache

from django.conf import settings

from .base import Embedder


@lru_cache(maxsize=1)
def get_embedder() -> Embedder:
    cfg = settings.RAG
    provider, model, dim = cfg["EMBEDDING_PROVIDER"], cfg["EMBEDDING_MODEL"], cfg["EMBEDDING_DIM"]
    if provider == "sentence-transformers":
        from .sentence_transformers import SentenceTransformersEmbedder

        return SentenceTransformersEmbedder(model, dim)
    if provider == "ollama":
        from .ollama import OllamaEmbedder

        return OllamaEmbedder(model, dim, cfg["OLLAMA_URL"])
    if provider == "openai":
        from .openai import OpenAIEmbedder

        return OpenAIEmbedder(model, dim, cfg["OPENAI_BASE_URL"], cfg["OPENAI_API_KEY"])
    if provider == "hash":
        from .hashing import HashingEmbedder

        return HashingEmbedder(dim)
    raise ValueError(f"Unknown RAG_EMBEDDING_PROVIDER: {provider}")
