"""Step 1 of RAG: turn a file into plain text (page by page)."""
from pathlib import Path

from pypdf import PdfReader


class UnsupportedFileType(ValueError):
    pass


def load_pages(path: str | Path) -> list[tuple[int | None, str]]:
    """Return [(page_number, text), ...]. Text files are a single page (None)."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        # Scanned PDFs have no text layer: run OCR (e.g. ocrmypdf) before ingesting.
        return [(i + 1, page.extract_text() or "") for i, page in enumerate(reader.pages)]
    if suffix in {".txt", ".md", ".markdown", ".rst"}:
        return [(None, path.read_text(encoding="utf-8", errors="ignore"))]
    raise UnsupportedFileType(f"Unsupported file type: {suffix}")
