SYSTEM_PROMPT = """You are a helpful assistant that answers ONLY from the provided context.
Rules:
- Use only facts from the CONTEXT. If the answer is not there, say you don't know.
- Cite sources with their numbers in square brackets, e.g. [1] or [2][3].
- Answer in the same language as the question. Be short and clear."""


def build_prompt(question: str, hits) -> str:
    blocks = []
    for n, h in enumerate(hits, start=1):
        where = f"{h.document}" + (f", page {h.page}" if h.page else "")
        blocks.append(f"[{n}] ({where})\n{h.text}")
    return "CONTEXT:\n" + "\n\n".join(blocks) + f"\n\nQUESTION: {question}\nANSWER:"
