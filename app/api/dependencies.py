from fastapi import Depends
from app.infrastructure.llm.factory import get_llm
from app.infrastructure.llm.local_adapter import LocalAdapter
from app.infrastructure.embeddings.embedding_service import LocalEmbeddingService
from app.infrastructure.vector_store.pgvector_repository import PgVectorRepository
from app.application.orchestrators.rag_orchestrator import RAGOrchestrator
from app.application.use_cases import IngestTextUseCase, QuerySimilarTextUseCase
from app.application.agents.financial_decision_engine import FinancialDecisionEngine
from app.config import settings


# -----------------------------
# Infrastructure
# -----------------------------

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


def get_llm_adapter():
    return get_llm()


# -----------------------------
# Use Cases
# -----------------------------

def get_ingest_use_case(
    embedding_service=Depends(get_embedding_service),
    vector_repository=Depends(get_vector_repository),
):
    return IngestTextUseCase(
        embedding_provider=embedding_service,
        vector_repository=vector_repository,
    )


def get_query_use_case(
    embedding_service=Depends(get_embedding_service),
    vector_repository=Depends(get_vector_repository),
):
    return QuerySimilarTextUseCase(
        embedding_provider=embedding_service,
        vector_repository=vector_repository,
    )


# -----------------------------
# Orchestrator + Agent
# -----------------------------

def get_orchestrator(
    repository=Depends(get_vector_repository),
    embedding_service=Depends(get_embedding_service),
    llm=Depends(get_llm_adapter),
):
    return RAGOrchestrator(
        repository=repository,
        embedding_service=embedding_service,
        llm=llm,
        fallback_llm=LocalAdapter(),
    )


def get_financial_engine(
    orchestrator=Depends(get_orchestrator),
):
    return FinancialDecisionEngine(orchestrator)
