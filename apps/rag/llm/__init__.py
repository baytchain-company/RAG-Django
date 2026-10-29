from functools import lru_cache

from django.conf import settings

from .base import LLM


@lru_cache(maxsize=1)
def get_llm() -> LLM:
    cfg = settings.RAG
    provider = cfg["LLM_PROVIDER"]
    if provider == "ollama":
        from .ollama import OllamaLLM

        return OllamaLLM(cfg["LLM_MODEL"], cfg["OLLAMA_URL"])
    if provider == "openai":
        from .openai_compat import OpenAICompatLLM

        return OpenAICompatLLM(cfg["LLM_MODEL"], cfg["OPENAI_BASE_URL"], cfg["OPENAI_API_KEY"])
    if provider == "none":
        from .extractive import ExtractiveLLM

        return ExtractiveLLM()
    raise ValueError(f"Unknown RAG_LLM_PROVIDER: {provider}")
