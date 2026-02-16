from pydantic import BaseModel
from typing import List
from uuid import UUID

class DocumentRequest(BaseModel):
    content: str

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class QueryResult(BaseModel):
    id: UUID
    content: str
    score: float

class QueryResponse(BaseModel):
    results: List[QueryResult]
