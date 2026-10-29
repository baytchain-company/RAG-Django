from django.conf import settings
from django.db import models
from pgvector.django import HnswIndex, VectorField


class Document(models.Model):
    """An uploaded source file (PDF, Markdown, TXT)."""

    title = models.CharField(max_length=255)
    source = models.CharField(max_length=500, blank=True, help_text="File name or URL")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Chunk(models.Model):
    """A small piece of a document plus its embedding (meaning coordinates)."""

    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="chunks")
    index = models.PositiveIntegerField(help_text="Position inside the document")
    page = models.PositiveIntegerField(null=True, blank=True)
    text = models.TextField()
    embedding = VectorField(dimensions=settings.RAG["EMBEDDING_DIM"])

    class Meta:
        ordering = ["document_id", "index"]
        indexes = [
            HnswIndex(
                name="chunk_embedding_hnsw",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            )
        ]

    def __str__(self):
        return f"{self.document.title} #{self.index}"
