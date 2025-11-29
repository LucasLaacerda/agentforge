from abc import ABC, abstractmethod
from typing import Optional, Any

class ProviderBase(ABC):
    """Adapter interface for LLM providers."""

    @abstractmethod
    async def generate(self, prompt: str, *, max_tokens: int = 512, functions: Optional[list]=None, stream: bool=False) -> dict:
        """
        Returns a standardized dict:
        {
          "text": str,
          "usage": {"prompt_tokens": int, "completion_tokens": int, "total_tokens": int},
          "function_call": {"name": str, "arguments": dict} | None,
          "raw": Any
        }
        """
        raise NotImplementedError
