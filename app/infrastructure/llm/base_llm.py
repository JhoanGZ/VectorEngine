class BaseLLM:
    supports_response_format: bool = False

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        response_format: dict | None = None
    ) -> str:
        raise NotImplementedError

