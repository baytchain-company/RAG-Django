from apps.rag.chunking import split_text


def test_short_text_is_one_chunk():
    assert split_text("Hello world.", chunk_size=100, overlap=0) == ["Hello world."]


def test_chunks_respect_size_and_overlap():
    text = " ".join(f"Sentence number {i}." for i in range(200))
    chunks = split_text(text, chunk_size=200, overlap=50)
    assert len(chunks) > 5
    assert all(len(c) <= 260 for c in chunks)  # size + overlap tail
    # overlap: the end of one chunk appears at the start of the next
    assert chunks[0].split()[-1] in chunks[1]


def test_empty_text():
    assert split_text("   ", chunk_size=100, overlap=10) == []
