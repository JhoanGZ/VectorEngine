import logging
import time
from fastapi import APIRouter, Depends, Request

from app.api.schemas import (
    FinancialRequest,
    FinancialResponse,
    DocumentRequest,
    QueryRequest,
    QueryResponse,
    QueryResult,
)

from app.api.dependencies import (
    get_financial_engine,
    get_ingest_use_case,
    get_query_use_case,
)

from app.application.agents.financial_decision_engine import FinancialDecisionEngine
from app.application.use_cases import (
    IngestTextUseCase,
    QuerySimilarTextUseCase,
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/documents")
def ingest_document(
    request: DocumentRequest,
    http_request: Request,
    use_case: IngestTextUseCase = Depends(get_ingest_use_case),
):
    request_id = http_request.state.request_id
    logger.info("document_ingest_started request_id=%s", request_id)

    use_case.execute(request.content)

    logger.info("document_ingest_completed request_id=%s", request_id)
    return {"status": "indexed"}


@router.post("/query", response_model=QueryResponse)
def query_similar(
    request: QueryRequest,
    http_request: Request,
    use_case: QuerySimilarTextUseCase = Depends(get_query_use_case),
):
    request_id = http_request.state.request_id

    logger.info(
        "query_received request_id=%s top_k=%d",
        request_id,
        request.top_k,
    )

    results = use_case.execute(request.query, request.top_k)

    logger.info(
        "query_completed request_id=%s results=%d",
        request_id,
        len(results),
    )

    return QueryResponse(
        results=[
            QueryResult(
                id=r["id"],
                content=r["content"],
                score=r["score"],
            )
            for r in results
        ]
    )


@router.get("/health", tags=["Health"])
def health(http_request: Request):
    request_id = http_request.state.request_id
    logger.info("health_check request_id=%s", request_id)

    return {
        "status": "ok",
        "service": "vectorengine",
    }


@router.post("/financial/analyze", response_model=FinancialResponse)
def analyze_financial(
    request: FinancialRequest,
    http_request: Request,
    engine: FinancialDecisionEngine = Depends(get_financial_engine),
):
    request_id = http_request.state.request_id
    start = time.perf_counter()

    logger.info(
        "financial_analysis_request_received request_id=%s",
        request_id,
    )

    try:
        result = engine.analyze(request.document)
        return result

    finally:
        duration = time.perf_counter() - start

        logger.info(
            "financial_analysis_completed request_id=%s duration_s=%.3f",
            request_id,
            duration,
        )
