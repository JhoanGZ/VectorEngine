# VectorEngine

VectorEngine is a backend semantic retrieval engine built with:

- Python 3.11+
- FastAPI
- PostgreSQL + pgvector
- sentence-transformers (local embeddings)

This project demonstrates clean architecture principles with replaceable infrastructure components.

## Features

- Local embedding generation (`all-MiniLM-L6-v2`)
- Semantic indexing
- Vector similarity search
- Clean layered architecture
- Dependency injection via FastAPI

---

## Setup

### 1. Start PostgreSQL (pgvector)

```bash
docker run --name vectordb \
  -e POSTGRES_PASSWORD=postgres \
  -p 5433:5432 \
  -d pgvector/pgvector:pg16

