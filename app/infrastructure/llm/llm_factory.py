from app.config import settings
from .openai_adapter import OpenAIAdapter
from .local_adapter import LocalAdapter


def get_llm():

    if not settings.LLM_PROVIDER:
        raise ValueError("LLM_PROVIDER is not configured.")

    providers = {
        "openai": OpenAIAdapter,
        "local": LocalAdapter,
        "claude": None,
        "gemini": None,
    }

    provider = settings.LLM_PROVIDER.lower()

    if provider not in providers:
        raise ValueError(f"Unsupported LLM provider: {provider}")

    adapter = providers[provider]

    if adapter is None:
        raise NotImplementedError(f"{provider} adapter not implemented yet.")

    return adapter()
