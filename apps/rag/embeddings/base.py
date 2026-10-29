from abc import ABC, abstractmethod


class Embedder(ABC):
    """Step 3 of RAG: text -> vector (coordinates of meaning)."""

    dim: int

    @abstractmethod
    def embed_documents(self, texts: list[str]) -> list[list[float]]: ...

    @abstractmethod
    def embed_query(self, text: str) -> list[float]: ...

    def _check(self, vectors: list[list[float]]) -> list[list[float]]:
        if vectors and len(vectors[0]) != self.dim:
            raise ValueError(
                f"Embedding size is {len(vectors[0])} but RAG_EMBEDDING_DIM={self.dim}. "
                "Set RAG_EMBEDDING_DIM to your model's size and recreate the database."
            )
        return vectors
