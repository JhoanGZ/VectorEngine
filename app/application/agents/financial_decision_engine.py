class FinancialDecisionEngine:

    def __init__(self, llm: BaseLLM, retrieval_service):
        self.llm = llm
        self.retrieval_service = retrieval_service

    def analyze(self, document: str) -> dict:
        context = self.retrieval_service.search(document)

        system_prompt = "You are a financial risk analysis AI..."
        user_prompt = f"""
        Context:
        {context}

        Document:
        {document}

        Respond ONLY in valid JSON format:
        {{
            "risk_score": float,
            "decision": "approve" | "review" | "reject",
            "key_risks": list[str],
            "summary": str
        }}
        """

        response = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.1,
            response_format={"type": "json_object"}
        )

        return json.loads(response)

