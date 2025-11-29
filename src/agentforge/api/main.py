# main.py (parte relevante)
import os
import importlib
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# carrega .env antes de qualquer coisa
load_dotenv()

from src.agentforge.providers.registry import REGISTRY

app = FastAPI(title="AgentForge (dev)")

PROVIDER = os.getenv("PROVIDER", "mock").lower()

def ensure_provider_registered(name: str):
    """
    Garante que o módulo do provider foi importado e que o decorator
    @register_provider executou, populando REGISTRY.
    """
    if name in REGISTRY:
        return

    # tenta importar o módulo provider — isso executa decorators e registra
    module_name = f"src.agentforge.providers.{name}_provider"
    try:
        importlib.import_module(module_name)
    except ModuleNotFoundError:
        # deixa o caller lidar com erro de provider inexistente
        return

@app.on_event("startup")
async def startup():
    provider_name = PROVIDER

    # sempre garantimos que o módulo foi importado (assim o decorator registra)
    ensure_provider_registered(provider_name)

    # se ainda não estiver no REGISTRY, fallback para 'mock'
    ProviderClass = REGISTRY.get(provider_name)
    if ProviderClass is None:
        # se for mock, tente registrar/importar explicitamente
        ensure_provider_registered("mock")
        ProviderClass = REGISTRY.get("mock")
        if ProviderClass is None:
            raise RuntimeError(f"No provider found for '{provider_name}', and no mock provider available.")
    # instancia e guarda no state
    app.state.provider = ProviderClass()

class GenRequest(BaseModel):
    prompt: str
    max_tokens: int = 256


@app.get("/health")
async def health():
    return {"status": "ok", "provider": PROVIDER}


@app.post("/generate")
async def generate(req: GenRequest):
    if not req.prompt:
        raise HTTPException(400, "prompt required")
    result = await app.state.provider.generate(req.prompt, max_tokens=req.max_tokens)
    return result
