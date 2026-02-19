from __future__ import annotations

from .base_llm import BaseLLM


class LocalAdapter(BaseLLM):
    """
    Local LLM adapter placeholder.

    This adapter is intentionally implemented as a safe stub until a real local
    inference backend is wired (e.g., Ollama, llama.cpp, vLLM).
    """

    supports_response_format = False

    def __init__(self, backend: str | None = None):
        # backend can be used later: "ollama", "llamacpp", etc.
        self.backend = backend or "stub"

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        response_format: dict | None = None,
    ) -> str:
        # Quality behavior: fail fast with a precise, helpful error
        raise RuntimeError(
            "LocalAdapter is configured but no local LLM backend is wired yet. "
            "Set LLM_PROVIDER=openai (recommended for now) or implement a local backend "
            "(e.g., Ollama) and update LocalAdapter.generate()."
        )

