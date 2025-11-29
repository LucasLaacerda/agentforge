import os
import asyncio
from openai import OpenAI
from .base import ProviderBase

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

from .registry import register_provider

@register_provider("openai")
class OpenAIProvider(ProviderBase):
    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found. Set it in your environment or pass api_key.")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model


    async def generate(
        self,
        prompt: str,
        *,
        max_tokens: int = 512,
        functions: list | None = None,
        stream: bool = False,
    ) -> dict:
        """
        Mantém a assinatura async. O cliente OpenAI atual é síncrono,
        então executamos a chamada em um thread separado para não bloquear.
        """

        def _sync_call():
            # chama a API nova (chat completions)
            return self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                functions=functions or None,
                temperature=0.2,
            )

        resp = await asyncio.to_thread(_sync_call)

        # tenta converter para dict para normalizar a resposta de forma consistente
        try:
            resp_dict = resp.to_dict()
        except Exception:
            try:
                resp_dict = dict(resp)
            except Exception:
                resp_dict = {}

        # extrai choice e message de maneira segura
        choice = resp_dict.get("choices", [{}])[0] if isinstance(resp_dict, dict) else {}
        message = choice.get("message", {}) if isinstance(choice, dict) else {}

        text = message.get("content", "") if isinstance(message, dict) else ""
        function_call = message.get("function_call") if isinstance(message, dict) else None
        usage = resp_dict.get("usage", {}) if isinstance(resp_dict, dict) else {}

        return {"text": text, "usage": usage, "function_call": function_call, "raw": resp}
