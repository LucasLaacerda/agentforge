from .base import ProviderBase
from .registry import register_provider

@register_provider("mock")
class MockProvider(ProviderBase):
    async def generate(self, prompt: str, **kwargs):
        text = f"MOCK RESPONSE — prompt length {len(prompt)}"
        return {
            "text": text,
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
            "function_call": None,
            "raw": {"mock": True}
        }
