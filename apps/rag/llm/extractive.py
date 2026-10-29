from .base import LLM


class ExtractiveLLM(LLM):
    """No model at all: returns the retrieved chunks. Handy to debug retrieval (RAG_LLM_PROVIDER=none)."""

    def generate(self, system, prompt):
        context = prompt.split("CONTEXT:", 1)[-1].split("QUESTION:", 1)[0].strip()
        return "Most relevant passages:\n\n" + context
