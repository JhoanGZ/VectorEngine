from .base_llm import BaseLLM

class LocalAdapter(BaseLLM):
    
    supports_response_format = False

    def generate(
        self.
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        response_format: dict | None = None
    ) -> str:

        return self.local_model_call(system_prompt, user_prompt)
