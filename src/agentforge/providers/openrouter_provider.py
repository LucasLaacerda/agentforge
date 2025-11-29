import os
import httpx
from typing import Optional, Any
from .base import ProviderBase


OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

from .registry import register_provider

@register_provider("openrouter")
class OpenRouterProvider(ProviderBase):
    """
    Provider usando OpenRouter.
    Compatível com chat/completions no estilo OpenAI.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or OPENROUTER_KEY
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY não encontrada no ambiente.")

        self.model = model
        self._client = httpx.AsyncClient(timeout=60.0)
        self.base_url = BASE_URL.rstrip("/")

    async def generate(
        self,
        prompt: str,
        *,
        max_tokens: int = 512,
        functions: Optional[list] = None,
        stream: bool = False,
    ) -> dict:

        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.2,
        }

        if functions:
            payload["functions"] = functions

        response = await self._client.post(url, headers=headers, json=payload)

        # Se vier erro HTTP, lança com o conteúdo
        if response.status_code >= 400:
            try:
                err = response.json()
            except Exception:
                err = response.text
            raise RuntimeError(f"OpenRouter error {response.status_code}: {err}")

        raw = response.json()

        # Normalização do formato
        text = ""
        function_call = None
        usage = raw.get("usage", {})

        choices = raw.get("choices", [])
        if choices:
            choice = choices[0]
            msg = choice.get("message", {}) or {}

            text = msg.get("content", "") or choice.get("text", "")
            function_call = msg.get("function_call") or choice.get("function_call")

        return {
            "text": text,
            "usage": usage,
            "function_call": function_call,
            "raw": raw,
        }
