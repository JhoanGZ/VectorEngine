from __future__ import annotations

from app.config import settings


def get_llm():
    provider = (settings.LLM_PROVIDER or "").lower().strip()

    if not provider:
        raise ValueError("LLM_PROVIDER is not configured.")

    if provider == "openai":
        # Lazy import: only imported when needed
        from .openai_adapter import OpenAIAdapter
        return OpenAIAdapter()

    if provider == "local":
        # Lazy import: only imported when needed
        from .local_adapter import LocalAdapter
        return LocalAdapter()

    raise ValueError(f"Unsupported LLM provider: {provider}")

