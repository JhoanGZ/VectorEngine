from __future__ import annotations

class BaseLLM:
    supports_response_format: bool = False

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        response_format: dict | None = None,
    ) -> str:
        raise NotImplementedError

