import requests

from .base import LLM


class OpenAICompatLLM(LLM):
    """OpenAI or any OpenAI-compatible API (Groq, OpenRouter, LM Studio, vLLM...)."""

    def __init__(self, model: str, base_url: str, api_key: str):
        self.model, self.base_url, self.api_key = model, base_url.rstrip("/"), api_key

    def generate(self, system, prompt):
        r = requests.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "temperature": 0.1,
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            },
            timeout=300,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
