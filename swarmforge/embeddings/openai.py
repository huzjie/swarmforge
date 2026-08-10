"""Openai embedding provider."""
from typing import List

class OpenaiEmbedder:
    def __init__(self, api_key: str = None, model: str = "default"):
        self.api_key = api_key
        self.model = model

    async def embed(self, texts: List[str]) -> List[List[float]]:
        return [[0.0] * 768 for _ in texts]

    async def embed_query(self, text: str) -> List[float]:
        return [0.0] * 768
