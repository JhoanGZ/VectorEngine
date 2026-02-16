# VectorEngine

VectorEngine is a fully containerized semantic retrieval engine built using production-oriented Clean Architecture principles.

It is designed as a reusable semantic retrieval core capable of powering higher-level systems such as CV tailoring engines, financial document analysis platforms, and structured knowledge retrieval services.

The project focuses on architectural clarity, replaceability, and engineering discipline.

---

## Engineering Objectives

- Strict layer separation (Domain / Application / Infrastructure / API)
- Dependency Inversion Principle (DIP)
- Infrastructure abstraction via domain contracts
- Swappable embedding providers
- Swappable vector store implementations
- Configurable retrieval policies (Top-K)
- Full containerization (API + Database)
- Reproducible development via Docker Compose

Phase 1 prioritizes correctness, clean boundaries, and reproducibility over premature optimization.

---

## Technical Scope & Engineering Intent

VectorEngine is grounded in modern Information Retrieval (IR) techniques and intentionally separates mathematical retrieval logic from infrastructure concerns.

The system implements:

- Dense embedding representations (384-dimensional vectors)
- Cosine similarity ranking
- Deterministic Top-K nearest neighbor retrieval
- Optional Approximate Nearest Neighbor (ANN) indexing via `ivfflat`

Architectural separation is explicit:

- Retrieval techniques (mathematical layer)
- Storage technology (`pgvector`)
- Application-level policies (Top-K configuration)

This design ensures the engine can evolve independently of specific storage technologies, embedding providers, or higher-level consumers.

The emphasis is on engineering discipline before optimization.

---

## Core Stack

- Python 3.10 (slim image)
- FastAPI
- PostgreSQL 16 + pgvector
- sentence-transformers (`all-MiniLM-L6-v2`)
- Torch (CPU build)
- Docker + Docker Compose

No external paid APIs are required for Phase 1.

---

## Architecture

```
app/
 ├── domain/
 │    ├── entities.py
 │    └── services.py
 │
 ├── application/
 │    └── use_cases.py
 │
 ├── infrastructure/
 │    ├── embeddings/
 │    └── vector_store/
 │
 ├── api/
 │    ├── routes.py
 │    ├── dependencies.py
 │    └── schemas.py
 │
 ├── config.py
 └── main.py
```

### Architectural Rules

- Domain does not depend on infrastructure
- Infrastructure implements domain contracts
- Dependencies point inward
- Embedding provider is replaceable
- Vector store is replaceable
- Retrieval policy (`top_k`) lives in the application layer
- API layer contains no business logic

---

## Design Decisions

### Embedding Model

- Model: `all-MiniLM-L6-v2`
- Vector dimension: **384**

The embedding dimension is explicitly aligned with the selected model.

Changing the embedding model requires regenerating stored embeddings.

### Vector Search Strategy

`pgvector` is used for similarity search.

Phase 1 favors deterministic exact search for clarity and predictability.

When dataset size grows, an `ivfflat` index can be enabled for ANN-based retrieval.

### Containerization Strategy

Both API and database run as isolated containers.

The system does not depend on a local Python environment and is reproducible with a single command.

---

## Running the System

### Start Services

```bash
docker compose up --build
```

This starts:

- `vectorengine_db` (PostgreSQL + pgvector)
- `vectorengine_api` (FastAPI application)

API available at:

```
http://localhost:8000
```

Swagger UI:

```
http://localhost:8000/docs
```

---

## API Endpoints

### GET /health

Returns service health status.

### POST /documents

Indexes a document by generating and storing embeddings.

### POST /query

Performs semantic similarity search using cosine distance and configurable Top-K retrieval.

---

## Phase 1 Status

Phase 1 delivers:

- Functional ingestion pipeline
- Semantic retrieval pipeline
- Strict architectural boundaries
- Full Docker reproducibility
- Verified end-to-end indexing and querying

---

## Engineering Philosophy

VectorEngine intentionally avoids premature abstraction and premature optimization.

It focuses first on:

- Clear dependency direction
- Replaceability
- Deterministic behavior
- Production-ready structure

This repository reflects deliberate backend engineering aimed at scalable semantic systems rather than prototype experimentation.

