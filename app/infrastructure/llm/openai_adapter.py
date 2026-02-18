class OpenAIAdapter(BaseLLM):

    def generate(
            self,
            system_prompt: str,
            user_prompt: str,
            temperature: float = 0.2,
            model: str = "gpt-4o-mini",
            response_format: dict | None = None
    ) -> str:
        try:
            response = self.client.chat.completions.create(
                    model=model,
                    temperate=temperature,
                    response_format=response_format,
                    messages=[
                        {"role": "system", "content": system_prompt}.
                        {"role": "user", "ccontent": user_prompt}
                    ],
            )
            return response.choices[0].message.content

        except Exception as e:
            raise RuntimeError(f"OpenAI LLM error: {str(e)}")

