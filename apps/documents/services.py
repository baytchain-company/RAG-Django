"""Ingestion: file -> text -> chunks -> embeddings -> database."""
from pathlib import Path

from django.db import transaction

from apps.rag.chunking import split_text
from apps.rag.embeddings import get_embedder

from .loaders import load_pages
from .models import Chunk, Document


@transaction.atomic
def ingest_text(title: str, pages: list[tuple[int | None, str]], source: str = "") -> Document:
    document = Document.objects.create(title=title, source=source)
    pieces = []  # (page, text)
    for page, text in pages:
        pieces += [(page, chunk) for chunk in split_text(text)]
    if not pieces:
        return document

    embedder = get_embedder()
    vectors = embedder.embed_documents([text for _, text in pieces])
    Chunk.objects.bulk_create(
        Chunk(document=document, index=i, page=page, text=text, embedding=vec)
        for i, ((page, text), vec) in enumerate(zip(pieces, vectors))
    )
    return document


def ingest_file(path: str | Path, title: str | None = None) -> Document:
    path = Path(path)
    return ingest_text(title or path.stem, load_pages(path), source=path.name)
