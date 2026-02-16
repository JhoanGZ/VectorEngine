# VectorEngine

VectorEngine is a fully containerized semantic retrieval engine built with production-oriented clean architecture principles.

It is designed as a reusable semantic retrieval core that can power higher-level systems such as CV tailoring engines, financial document analysis tools, and structured knowledge retrieval services.

---

## Engineering Objectives

This project demonstrates:

- Clean Architecture with strict layer separation
- Dependency Inversion Principle (DIP)
- Replaceable embedding providers
- Replaceable vector store implementations
- Fully containerized API and database
- Configurable retrieval policies (Top-K)
- Reproducible development environment via Docker Compose

Phase 1 prioritizes correctness, architectural integrity, and reproducibility over premature optimization.

---

## Technical Foundations

VectorEngine is grounded in modern Information Retrieval (IR) techniques:

- Dense vector embeddings for semantic representation
- Cosine similarity distance for ranking
- Top-K nearest neighbor retrieval
- Optional Approximate Nearest Neighbor (ANN) indexing via `ivfflat`

The system explicitly separates:

- Retrieval techniques (mathematical layer)
- Storage technology (pgvector)
- Application-level policies (Top-K configuration)

This allows the engine to evolve independently from specific infrastructure choices.

---

## Core Stack

- Python 3.10 (slim image)
- FastAPI
- PostgreSQL 16 + pgvector
- sentence-transformers (`all-MiniLM-L6-v2`)
- Torch (CPU build)
- Docker + Docker Compose

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
- Embedding provider is swappable
- Vector store is swappable
- Retrieval policy (`top_k`) lives in the application layer

---

## Design Decisions

### Embedding Model

- Model: `all-MiniLM-L6-v2`
- Vector dimension: **384**

The embedding dimension is explicitly aligned with the selected model.

Changing the embedding model requires regenerating stored embeddings.

### Vector Search Strategy

pgvector is used for similarity search.

Phase 1 prioritizes clarity and deterministic behavior.

An `ivfflat` index can be enabled for approximate nearest neighbor (ANN) search when dataset size grows. For small datasets, exact scans are sufficient and simpler.

### Containerization Strategy

Both API and database run as isolated containers.

The application does not depend on a local Python environment. The system is reproducible using a single command.

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

### Health Check

```
GET /health
```

Response:

```json
{
  "status": "ok",
  "service": "vectorengine"
}
```

---

### Index Document

```
POST /documents
```

Body:

```json
{
  "content": "VectorEngine test document."
}
```

Response:

```json
{
  "status": "indexed"
}
```

---

### Query Similar Documents

```
POST /query
```

Body:

```json
{
  "query": "VectorEngine",
  "top_k": 1
}
```

Response:

```json
{
  "results": [
    {
      "id": "uuid",
      "content": "Stored text",
      "score": 0.703
    }
  ]
}
```

Lower cosine distance indicates higher semantic similarity.

---

## Database Initialization

The database container initializes automatically using:

```
./init.sql
```

This sets up:

- `vector` extension
- `document_chunks` table
- Optional `ivfflat` index

Persistent data is stored in a Docker volume:

```
pgdata
```

---

## Docker Image Details

### Base Image

```
python:3.10-slim
```

### Dependency Installation Strategy

- Torch CPU build installed explicitly
- Python dependencies installed via `requirements.txt`
- Layer caching optimized by copying `requirements.txt` before source code

### .dockerignore

The `.dockerignore` file prevents unnecessary files from entering the build context:

- `venv/`
- `__pycache__/`
- `.git/`
- Local artifacts

This reduces image size and prevents unnecessary cache invalidation.

---

## Phase 1 Status

Phase 1 delivers:

- Functional ingestion pipeline
- Semantic retrieval pipeline
- Full containerization
- Clean architecture boundaries
- Configurable retrieval policies

The system is stable and operational inside Docker Compose.

## Verified Capabilities

- End-to-end ingestion tested
- End-to-end retrieval tested
- Docker reproducibility verified
- Health endpoint verified

Future improvements may include:

- ANN parameter tuning (`lists`, `probes`)
- Benchmarking
- Multi-stage Docker optimization
- CI/CD integration
- Background ingestion workers

---

## Engineering Philosophy

VectorEngine prioritizes architectural clarity over premature optimization.

It is intentionally minimal in Phase 1, focusing on correctness, replaceability, and clean dependency direction before performance refinement.

This project reflects disciplined backend engineering and a deliberate approach to scalable semantic systems.


