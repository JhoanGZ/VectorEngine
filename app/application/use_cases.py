class QueryDocumentUseCase:

    def __init__(self, embedding_provider: EmbeddingProvider,
            vector_repository: VectorRepository):
        self.embedding_provider = embedding_provider
        self.vector_repository = vector_repository

    
    def execute(self, query: str, k: int = 5):
        query_embedding = self.embedding_provider.generate_embedding(query)
        return self.vector_repository.similarity_search(query_embedding, k)


