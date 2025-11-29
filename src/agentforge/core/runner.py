# small runner pattern to centralize orchestration (placeholder)
from typing import Any
from agentforge.providers.base import ProviderBase

class Runner:
    def __init__(self, provider: ProviderBase):
        self.provider = provider

    async def ask(self, prompt: str, **kwargs) -> dict:
        return await self.provider.generate(prompt, **kwargs)
