# Django RAG

A small, readable **Retrieval-Augmented Generation** project built with Django, Django REST Framework and PostgreSQL + **pgvector**.
Upload PDFs or text files, ask questions, and get answers **only from your documents, with sources**.

Free by default: local embeddings (`sentence-transformers`) and a local LLM (`Ollama`). No API key needed.

> 🇺🇿 O'zbekcha qisqacha qo'llanma pastda.

---

## How it works

```
             INGEST                                       ASK
 file ─▶ loaders.py ─▶ chunking.py ─▶ embeddings/ ─▶  PostgreSQL + pgvector
 (pdf/md)  (text)       (chunks)       (vectors)              │
                                                              ▼
 question ─▶ embeddings/ ─▶ retriever.py ─▶ prompts.py ─▶ llm/ ─▶ answer + [sources]
             (query vector)  (top-k closest)  (context)    (Ollama / OpenAI / none)
```

| Step | What happens | File |
|---|---|---|
| 1. Load | File → plain text (page by page) | `apps/documents/loaders.py` |
| 2. Chunk | Text → overlapping pieces | `apps/rag/chunking.py` |
| 3. Embed | Each chunk → vector of numbers (meaning) | `apps/rag/embeddings/` |
| 4. Store | Vectors saved in Postgres (HNSW index) | `apps/documents/models.py` |
| 5. Retrieve | Question → vector → closest chunks (cosine distance) | `apps/rag/retriever.py` |
| 6. Generate | Chunks + question → LLM → answer with `[1]` citations | `apps/rag/prompts.py`, `apps/rag/llm/` |
| — | The whole flow in one function | `apps/rag/pipeline.py` |

## Project structure

```
django-rag/
├── config/                  # Django settings, urls, wsgi/asgi
├── apps/
│   ├── documents/           # Document + Chunk models, file loaders, ingestion service
│   │   └── management/commands/ingest.py
│   ├── rag/                 # The RAG core (no HTTP code here)
│   │   ├── chunking.py
│   │   ├── embeddings/      # sentence-transformers | ollama | openai | hash
│   │   ├── llm/             # ollama | openai-compatible | extractive (no LLM)
│   │   ├── retriever.py
│   │   ├── prompts.py
│   │   ├── pipeline.py
│   │   └── management/commands/ask.py
│   └── api/                 # REST API (DRF): upload documents, ask questions
├── templates/index.html     # Minimal web UI
├── data/sample/             # Example documents (fictional company handbook, EN + UZ)
├── tests/                   # pytest (runs offline: hash embedder + no LLM)
├── docker-compose.yml       # PostgreSQL 16 with pgvector
├── requirements.txt
└── .env.example
```

## Quick start

Requirements: Python 3.11+, Docker (for the database), and optionally [Ollama](https://ollama.com) for answers.

```bash
# 1. Database (Postgres + pgvector)
docker compose up -d

# 2. Python environment
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# 3. Local LLM (free)
ollama pull llama3.2

# 4. Create tables and load the sample documents
python manage.py migrate
python manage.py ingest data/sample

# 5. Ask
python manage.py ask "How many vacation days do I get?"
python manage.py runserver          # then open http://127.0.0.1:8000
```

The first `ingest` downloads the embedding model `intfloat/multilingual-e5-small` (~470 MB, once). It supports ~100 languages, including Uzbek.

## REST API

```bash
# Upload a file
curl -F "file=@my.pdf" http://127.0.0.1:8000/api/documents/

# Or raw text
curl -H "Content-Type: application/json" \
     -d '{"title": "Notes", "text": "Salaries are paid on the 5th."}' \
     http://127.0.0.1:8000/api/documents/

# Ask
curl -H "Content-Type: application/json" \
     -d '{"question": "When are salaries paid?", "top_k": 4}' \
     http://127.0.0.1:8000/api/ask/
```

Response:

```json
{
  "question": "When are salaries paid?",
  "answer": "Salaries are paid on the 5th of every month [1].",
  "sources": [{"n": 1, "document": "company_handbook_en", "page": null, "index": 2, "distance": 0.18, "text": "..."}]
}
```

Other endpoints: `GET /api/documents/`, `DELETE /api/documents/<id>/`, Django admin at `/admin/`.

## Switching providers (`.env`)

| Want | Set |
|---|---|
| Free local embeddings (default) | `RAG_EMBEDDING_PROVIDER=sentence-transformers`, `RAG_EMBEDDING_DIM=384` |
| Ollama embeddings | `RAG_EMBEDDING_PROVIDER=ollama`, `RAG_EMBEDDING_MODEL=nomic-embed-text`, `RAG_EMBEDDING_DIM=768` |
| OpenAI embeddings | `RAG_EMBEDDING_PROVIDER=openai`, `RAG_EMBEDDING_MODEL=text-embedding-3-small`, `RAG_EMBEDDING_DIM=1536`, `OPENAI_API_KEY=...` |
| OpenAI / Groq / OpenRouter for answers | `RAG_LLM_PROVIDER=openai`, `OPENAI_BASE_URL=...`, `RAG_LLM_MODEL=...`, `OPENAI_API_KEY=...` |
| Debug retrieval without any LLM | `RAG_LLM_PROVIDER=none` (returns the found chunks) |
| Zero downloads (demo only) | `RAG_EMBEDDING_PROVIDER=hash` (matches words, not meaning) |

⚠️ `RAG_EMBEDDING_DIM` must match the model. If you change it, recreate the database (`docker compose down -v`, then `migrate` and `ingest` again).

## Tuning

- `RAG_CHUNK_SIZE` / `RAG_CHUNK_OVERLAP` — chunking is the biggest quality lever. Too big = noisy context, too small = lost meaning.
- `RAG_TOP_K` — how many chunks go to the model.
- `RAG_MAX_DISTANCE` — chunks farther than this are ignored, so the model says "not found" instead of guessing.

## Tests

```bash
pytest
```

Tests need the database running (`docker compose up -d`), but no model downloads or API keys.

## Troubleshooting

- **`type "vector" does not exist`** — use the `pgvector/pgvector` image from `docker-compose.yml` (plain Postgres lacks the extension).
- **Embedding size mismatch** — set `RAG_EMBEDDING_DIM` to your model's size and recreate the database.
- **Scanned PDF returns no text** — it has no text layer; run OCR first (e.g. `ocrmypdf in.pdf out.pdf`).
- **Ollama connection refused** — start Ollama (`ollama serve`) or set `RAG_LLM_PROVIDER=openai`/`none`.

---

## 🇺🇿 O'zbekcha qisqacha

Bu loyiha hujjatlaringiz (PDF, Markdown, TXT) asosida savollarga **faqat hujjatdagi ma'lumotdan, manbasi bilan** javob beradi.

```bash
docker compose up -d                 # Postgres + pgvector
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
ollama pull llama3.2                 # bepul lokal model
python manage.py migrate
python manage.py ingest data/sample  # namuna hujjatlar
python manage.py ask "Yiliga necha kun ta'til beriladi?"
python manage.py runserver           # http://127.0.0.1:8000
```

Qanday ishlaydi: fayl → matn → bo'laklar (chunk) → embedding (raqamlar) → pgvector'da saqlanadi.
Savol ham raqamga aylanadi, eng yaqin bo'laklar topiladi va model faqat shu bo'laklar asosida javob yozadi.

Made by [@dev.baytchain](https://instagram.com/dev.baytchain) · MIT License
# RAG-Django
