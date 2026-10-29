"""The whole RAG flow in one function: question -> retrieve -> prompt -> LLM -> answer with sources."""
from dataclasses import asdict

from .llm import get_llm
from .prompts import SYSTEM_PROMPT, build_prompt
from .retriever import retrieve

NOT_FOUND = "I couldn't find this in the documents. / Hujjatlarda bu haqida ma'lumot topilmadi."


def ask(question: str, top_k: int | None = None) -> dict:
    question = question.strip()
    hits = retrieve(question, top_k=top_k)
    if not hits:  # never let the model guess without context
        return {"question": question, "answer": NOT_FOUND, "sources": []}

    answer = get_llm().generate(SYSTEM_PROMPT, build_prompt(question, hits))
    sources = [{"n": n, **asdict(h)} for n, h in enumerate(hits, start=1)]
    return {"question": question, "answer": answer, "sources": sources}
