# VectorEngine

**Production-oriented AI infrastructure backend for semantic retrieval, LLM orchestration, and algorithmic decision systems.**

VectorEngine is a containerized backend core designed for building resilient, real-world AI systems.  
It is not a chatbot wrapper. It is not a prototype.

It is infrastructure.

---

## Overview

VectorEngine solves three core problems in modern AI engineering:

1. Deterministic semantic retrieval  
2. Resilient multi-provider LLM orchestration  
3. Algorithmic decision execution

It is designed to power systems such as:

- Financial document analysis engines  
- CV intelligence and structured matching platforms  
- Knowledge retrieval services  
- Allocation and decision-support systems

The emphasis is architectural clarity, replaceability, and operational resilience.

---

# Core Capabilities

## 1️⃣ Dense Semantic Retrieval

- 384-dimensional embeddings (`all-MiniLM-L6-v2`)
- Cosine similarity via PostgreSQL + pgvector
- Deterministic Top-K retrieval
- ANN-ready via `ivfflat`

Retrieval logic is separated from storage and API layers.

---

## 2️⃣ RAG Orchestration Layer

The `RAGOrchestrator` executes:

```
Query → Embedding → Similarity Search → Context Assembly → Prompt Construction → LLM Invocation → Structured Response
```

Guarantees:

- Provider-agnostic orchestration
- Structured JSON enforcement
- Automatic provider fallback
- Deterministic local execution for CI

Supported providers:

| Provider | Role |
|-----------|------|
| `OpenAIAdapter` | Primary |
| `LocalAdapter` | Deterministic fallback |

If the primary provider fails, fallback is triggered automatically without breaking API contracts.

---

## 3️⃣ Financial Decision Engine

A domain-level AI agent built on top of the RAG core.

- Enforces structured output schema
- Parses and validates LLM responses
- Returns typed financial risk assessments

Example response:

```json
{
  "risk_score": 0.41,
  "decision": "review",
  "key_risks": ["insufficient historical data"],
  "summary": "Financial analysis summary..."
}
```

Predictable AI behavior under contract enforcement.

---

## 4️⃣ Stable Matching Engine (Phase 2)

VectorEngine includes a generic Gale–Shapley stable matching engine.

Endpoint:

```
POST /matching/run
```

Input:
- Group A entities with ranked preferences
- Group B entities with ranked preferences

Output:
- Stable allocation (no blocking pairs)

Use cases:
- Candidate ↔ role matching
- Portfolio ↔ risk allocation
- Structured preference-based assignment

This demonstrates deterministic allocation logic independent of LLM inference.

---

## 5️⃣ Streaming LLM Endpoint (Phase 2)

```
GET /analysis/stream
```

Implemented using FastAPI async generators.

Enables:
- Token streaming simulation
- Progressive response delivery
- Foundation for real-time AI interfaces

---

## 6️⃣ Observability & Resilience

Every request includes:

- `request_id` correlation
- Endpoint-level latency logging
- Provider-level invocation logging
- Fallback tracing

Example log flow:

```
request_started request_id=...
llm_invocation provider=OpenAIAdapter
primary_llm_failed provider=OpenAIAdapter
fallback_to_provider provider=LocalAdapter
llm_completed provider=LocalAdapter duration_s=0.018
request_finished request_id=... status_code=200
```

The system does not fail silently.

---

# Architecture

```
app/
 ├── domain/                # Contracts and entities (no external dependencies)
 ├── application/
 │    ├── use_cases/
 │    ├── orchestrators/
 │    └── agents/
 ├── infrastructure/
 │    ├── embeddings/
 │    ├── vector_store/
 │    └── llm/
 ├── api/
 │    ├── routes.py
 │    ├── dependencies.py   # Composition root
 │    └── schemas.py
 ├── core/                  # Logging & tracing middleware
 ├── config.py
 └── main.py
```

## Architectural Rules

- Domain imports nothing external
- Application layer is infrastructure-agnostic
- Infrastructure implements domain contracts
- API layer contains no business logic
- Fallback strategy lives in the orchestrator
- Retrieval policy belongs to the application layer

---

# Tech Stack

- Python 3.10 (slim)
- FastAPI + Uvicorn
- PostgreSQL 16 + pgvector
- sentence-transformers (`all-MiniLM-L6-v2`)
- Torch (CPU build)
- Optional OpenAI API
- Docker + Docker Compose

Runs fully offline using `LLM_PROVIDER=local`.

---

# Running

```bash
docker compose up --build
```

API:
```
http://localhost:8000
```

Swagger:
```
http://localhost:8000/docs
```

---

# Roadmap

## Phase 2

- Stable matching engine integration
- Streaming token support
- Extended observability
- CI/CD automation
- Performance benchmarking

Future considerations:

- Cloud deployment
- Concurrency tuning
- Voice / real-time pipelines
- Horizontal scaling

---

# Engineering Philosophy

VectorEngine prioritizes:

- Replaceability over coupling
- Determinism over hype
- Explicit orchestration over hidden abstraction
- Infrastructure discipline over demo engineering

This project reflects backend AI systems engineering designed for scalable, resilient, and production-ready intelligent platforms.


