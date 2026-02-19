import json

class FinancialDecisionEngine:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def analyze(self, document: str) -> dict:
        system_prompt = (
            "You are a financial decision intelligence system operating "
            "inside public infrastructure. Provide structured risk analysis."
        )
        user_template = """
        Context:
        {context}
        Document:
        {query}
        Respond ONLY in valid JSON format:
        {{
            "risk_score": float between 0 and 1,
            "decision": "approve" | "review" | "reject",
            "key_risks": list of strings,
            "summary": string
        }}
        """
        response_format = (
            {"type": "json_object"}
            if getattr(self.orchestrator.llm, "supports_response_format", False)
            else None
        )

        raw_response = self.orchestrator.execute(
            query=document,
            system_prompt=system_prompt,
            user_instruction_template=user_template,
            response_format=response_format,
            temperature=0.1,
        )

        try:
            return json.loads(raw_response)
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM returned invalid JSON: {e}\nResponse: {raw_response}")
