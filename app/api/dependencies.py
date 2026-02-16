from app.infrastructure.embeddings.embedding_service import LocalEmbeddingService
from app.infrastructure.vector_store.pgvector_repository import PgVectorRepository
from app.application.use_cases import IngestTextUseCase, QuerySimilarTextUseCase
from app.config import settings


def get_embedding_service():
    return LocalEmbeddingService()


def get_vector_repository():
    return PgVectorRepository(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        db_name=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
    )

def get_ingest_use_case():
    return IngestTextUseCase(
        embedding_provider=get_embedding_service(),
        vector_repository=get_vector_repository(),
    )


def get_query_use_case():
    return QuerySimilarTextUseCase(
        embedding_provider=get_embedding_service(),
        vector_repository=get_vector_repository(),
    )

