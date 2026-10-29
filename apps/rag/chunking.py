"""Step 2 of RAG: split text into overlapping chunks.

Too big  -> the search finds the right chunk but it is full of noise.
Too small -> a chunk loses its context ("it costs $5" — what costs $5?).
"""
import re

from django.conf import settings

_SEPARATORS = ["\n\n", "\n", ". ", "? ", "! ", "; ", ", ", " "]


def _split(text: str, size: int, seps: list[str]) -> list[str]:
    if len(text) <= size:
        return [text]
    if not seps:  # no separator left: hard cut
        return [text[i : i + size] for i in range(0, len(text), size)]
    sep, rest = seps[0], seps[1:]
    parts = text.split(sep)
    out = []
    for i, part in enumerate(parts):
        piece = part + (sep if i < len(parts) - 1 else "")
        out += _split(piece, size, rest) if len(piece) > size else [piece]
    return out


def split_text(text: str, chunk_size: int | None = None, overlap: int | None = None) -> list[str]:
    cfg = settings.RAG
    size = chunk_size or cfg["CHUNK_SIZE"]
    overlap = cfg["CHUNK_OVERLAP"] if overlap is None else overlap
    text = re.sub(r"[ \t]+", " ", text).strip()
    if not text:
        return []

    chunks, current = [], ""
    for piece in _split(text, size, _SEPARATORS):
        if len(current) + len(piece) <= size:
            current += piece
            continue
        if current.strip():
            chunks.append(current.strip())
        # start the next chunk with the tail of the previous one (keeps context)
        tail = current[-overlap:] if overlap else ""
        if " " in tail:
            tail = tail[tail.index(" ") + 1 :]
        current = tail + piece
    if current.strip():
        chunks.append(current.strip())
    return chunks
