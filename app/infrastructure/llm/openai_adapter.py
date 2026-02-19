from openai import OpenAI
from app.config import settings
from .base_llm import BaseLLM


class OpenAIAdapter(BaseLLM):

    supports_response_format = True
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def generate(
            self,
            system_prompt: str,
            user_prompt: str,
            temperature: float = 0.2,
            model: str = "gpt-4o-mini",
            response_format: dict | None = None
    ) -> str:
        try:
            kwargs = {
                "model": model,
                "temperature": temperature,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            }

            if response_format:
                kwargs["response_format"] = response_format
            
            response = self.client.chat.completions.create(**kwargs)

            return response.choices[0].message.content

        except Exception as e:
            raise RuntimeError(f"OpenAI LLM error: {str(e)}")














