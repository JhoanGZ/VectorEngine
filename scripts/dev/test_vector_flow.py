import uuid
from app.infrastructure.embeddings.embedding_service import LocalEmbeddingService
from app.infrastructure.vector_store.pgvector_repository import PgVectorRepository


embedder = LocalEmbeddingService()
repo = PgVectorRepository()

texts = [
    "financial report Q4 profit growth",
    "annual revenue analysis and projections",
    "machine learning model optimization",
]

# Insert documents
for text in texts:
    embedding = embedder.generate_embedding(text)
    repo.save(str(uuid.uuid4()), text, embedding)

print("Inserted documents.")

# Query similarity
query = "financial profit increase"
query_embedding = embedder.generate_embedding(query)

results = repo.similarity_search(query_embedding, k=2)

print("\nTop 2 similar results:")
for r in results:
    print(r)

