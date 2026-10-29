"""Test settings: offline embedder + no LLM, so tests run without downloads or API keys."""
from config.settings import *  # noqa: F401,F403

RAG = {**RAG, "EMBEDDING_PROVIDER": "hash", "LLM_PROVIDER": "none", "MAX_DISTANCE": 1.5}  # noqa: F405
