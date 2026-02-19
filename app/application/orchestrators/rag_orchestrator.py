class RAGOrchestrator:

    def __init__(self, repository, embedding_service, llm):
        self.repository = repository
        self.embedding_service = embedding_service
        self.llm = llm
    
    def execute(
        self,
        query: str,
        system_prompt: str,
        user_instruction_template: str,
        top_k: int = 5,
        temperature: float = 0.1,
        response_format: dict | None = None,
    ) -> str:

        embedding = self.embedding_service.generate_embedding(query)
        results = self.repository.similarity_search(embedding, top_k)

        if not results:
            context = "No relevant documents retrieved from knowledge base."
        else:
            context = "\n\n".join(
                [r["content"] for r in results if r.get("content")]
            )

        user_prompt = user_instruction_template.format(
            context=context,
            query=query,
        )
        
        if response_format and not getattr(self.llm, "supports_response_format", False):
            response_format = None

        return self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            response_format=response_format,
        )

