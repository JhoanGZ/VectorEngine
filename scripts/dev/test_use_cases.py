from app.infrastructure.embeddings.embedding_service import LocalEmbeddingService
from app.infrastructure.vector_store.pgvector_repository import PgVectorRepository
from app.application.use_cases import IngestTextUseCase, QuerySimilarTextUseCase


embedder = LocalEmbeddingService()
repo = PgVectorRepository()

ingest = IngestTextUseCase(embedder, repo)
query_uc = QuerySimilarTextUseCase(embedder, repo)

texts = [
    "financial report Q4 profit growth",
    "annual revenue analysis and projections",
    "machine learning model optimization",
]

for t in texts:
    ingest.execute(t)

results = query_uc.execute("financial profit increase", k=2)

print("Top results:")
for r in results:
    print(r)

