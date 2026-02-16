from fastapi import APIRouter, Depends
from app.api.schemas import (
    DocumentRequest,
    QueryRequest,
    QueryResponse,
    QueryResult,
)
from app.api.dependencies import (
    get_ingest_use_case,
    get_query_use_case,
)
from app.application.use_cases import (
    IngestTextUseCase,
    QuerySimilarTextUseCase,
)

router = APIRouter()


@router.post("/documents")
def ingest_document(
    request: DocumentRequest,
    use_case: IngestTextUseCase = Depends(get_ingest_use_case),
):
    use_case.execute(request.content)
    return {"status": "indexed"}


@router.post("/query", response_model=QueryResponse)
def query_similar(
    request: QueryRequest,
    use_case: QuerySimilarTextUseCase = Depends(get_query_use_case),
):
    results = use_case.execute(request.query, request.top_k)

    return QueryResponse(
        results=[
            QueryResult(
                id=r["id"],
                content=r["content"],
                score=r["score"]
            )
            for r in results
        ]
    )

