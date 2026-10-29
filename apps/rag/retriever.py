"""Step 4 of RAG: find the chunks closest in meaning to the question (pgvector)."""
from dataclasses import dataclass

from django.conf import settings
from pgvector.django import CosineDistance

from apps.documents.models import Chunk

from .embeddings import get_embedder


@dataclass
class Hit:
    chunk_id: int
    document: str
    page: int | None
    index: int
    text: str
    distance: float


def retrieve(question: str, top_k: int | None = None, max_distance: float | None = None) -> list[Hit]:
    cfg = settings.RAG
    top_k = top_k or cfg["TOP_K"]
    max_distance = cfg["MAX_DISTANCE"] if max_distance is None else max_distance

    query_vector = get_embedder().embed_query(question)
    qs = (
        Chunk.objects.select_related("document")
        .annotate(distance=CosineDistance("embedding", query_vector))
        .filter(distance__lte=max_distance)
        .order_by("distance")[:top_k]
    )
    return [
        Hit(c.id, c.document.title, c.page, c.index, c.text, round(float(c.distance), 4))
        for c in qs
    ]
