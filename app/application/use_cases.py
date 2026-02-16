import uuid

class IngestTextUseCase:

    def __init__(self, embedding_provider, vector_repository):
        self.embedding_provider = embedding_provider
        self.vector_repository = vector_repository

    def execute(self, content: str):
        embedding = self.embedding_provider.generate_embedding(content)
        chunk_id = str(uuid.uuid4())
        self.vector_repository.save(chunk_id, content, embedding)

class QuerySimilarTextUseCase:

    def __init__(self, embedding_provider, vector_repository):
        self.embedding_provider = embedding_provider
        self.vector_repository = vector_repository

    def execute(self, query: str, k: int = 5):
        query_embedding = self.embedding_provider.generate_embedding(query)
        return self.vector_repository.similarity_search(query_embedding, k)

