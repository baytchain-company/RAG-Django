import requests

from .base import LLM


class OllamaLLM(LLM):
    """Free and local: install Ollama, then `ollama pull llama3.2`."""

    def __init__(self, model: str, url: str):
        self.model, self.url = model, url.rstrip("/")

    def generate(self, system, prompt):
        r = requests.post(
            f"{self.url}/api/chat",
            json={
                "model": self.model,
                "stream": False,
                "options": {"temperature": 0.1},
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            },
            timeout=300,
        )
        r.raise_for_status()
        return r.json()["message"]["content"].strip()
