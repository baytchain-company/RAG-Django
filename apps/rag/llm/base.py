from abc import ABC, abstractmethod


class LLM(ABC):
    """Step 5 of RAG: write the answer from the retrieved chunks."""

    @abstractmethod
    def generate(self, system: str, prompt: str) -> str: ...
