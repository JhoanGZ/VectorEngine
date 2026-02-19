# ARCHITECTURE.md

# VectorEngine — Architecture Documentation

**Version:** 1.5  
**Status:** Stable (Resilient Core + RAG + Observability)

---

# 1. Architectural Philosophy

VectorEngine is designed following strict Clean Architecture principles.

The system enforces:

- Inward dependency flow
- Infrastructure replaceability
- Explicit orchestration layer
- Deterministic retrieval behavior
- Observability-first backend design

The goal is not to build a demo RAG system, but a replaceable AI infrastructure core.

---

# 2. Layered Structure

```bash
app/
├── domain/
│   ├── entities.py
│   └── contracts.py
│
├── application/
│   ├── use_cases/
│   ├── agents/
│   └── orchestrators/
│
├── infrastructure/
│   ├── embeddings/
│   ├── llm/
│   └── vector_store/
│
├── api/
│   ├── routes.py
│   ├── dependencies.py
│   └── schemas.py
│
├── core/
│   └── logging.py
│
├── config.py
└── main.py
```

---

# 3. Dependency Direction

Dependencies follow strict inward flow:

```
API → Application → Domain
Infrastructure → Domain
```

- Domain never depends on infrastructure
- Application never depends on concrete providers
- Infrastructure implements domain contracts
- API contains zero business logic

---

# 4. Core Components

## 4.1 RAGOrchestrator

**Responsibilities:**

- Generate embedding for query
- Perform similarity search (Top-K)
- Build contextual prompt
- Invoke LLM
- Handle provider capability (`structured output` support)
- Execute fallback strategy if primary LLM fails
- Emit structured observability logs

**The orchestrator does not:**

- Know about HTTP
- Know about database internals
- Parse JSON responses

It is orchestration-only.

---

## 4.2 LLM Abstraction

```
BaseLLM
├── OpenAIAdapter
└── LocalAdapter (deterministic fallback)
```

**Design decisions:**

- Providers are swappable
- Capability flag: `supports_response_format`
- Failure isolation inside orchestrator
- Graceful degradation via LocalAdapter

This enables:

- Production provider
- Development mode
- CI deterministic execution

---

## 4.3 Embedding Layer

Embedding provider is abstracted.

**Current implementation:**
- sentence-transformers
- 384-dimensional vectors

Swappable without changing application logic.

---

## 4.4 Vector Store

**Repository abstraction:**
- PgVectorRepository

**Features:**
- Cosine similarity search
- Deterministic Top-K
- ANN-ready (ivfflat optional)

Storage can be replaced without touching domain logic.

---

# 5. FinancialDecisionEngine

This agent:

- Constructs system prompt
- Defines structured response schema
- Delegates execution to RAGOrchestrator
- Parses LLM output
- Returns strongly typed response

**Separation ensures:**

- Agent contains domain logic
- Orchestrator contains AI orchestration
- Infrastructure contains provider details

---

# 6. Resilience Strategy

VectorEngine implements:

1. Primary LLM invocation
2. Structured logging of latency
3. Failure capture
4. Automatic fallback to deterministic local provider
5. Final error escalation only if fallback fails

This guarantees:

- No silent crashes
- Predictable behavior under quota exhaustion
- Observable failure modes

---

# 7. Observability Model

Each request generates:

- `request_id` (UUID)
- Route-level timing
- Orchestrator-level timing
- Provider-level logs
- Fallback detection logs

**Example log flow:**

```text
financial_analysis_request_received request_id=...
llm_invocation provider=OpenAIAdapter structured=True
primary_llm_failed provider=OpenAIAdapter
fallback_to_local_adapter
llm_completed provider=LocalAdapter duration_s=0.000
financial_analysis_completed request_id=... duration_s=0.084
request_finished request_id=... status_code=200
```

This allows:

- Latency tracing
- Provider performance measurement
- Failure frequency analysis
- Production diagnostics

---

# 8. Deployment Model

Containerized via Docker Compose:

- API container
- PostgreSQL + pgvector container

Environment-based provider selection:

```bash
LLM_PROVIDER=openai | local
```

System behavior changes without code modification.

---

# 9. Non-Goals (Phase 1.5)

- Horizontal scaling
- Async streaming responses
- Distributed caching
- Load balancing
- Circuit breakers
- Metrics exporters (Prometheus)

These are reserved for Phase 2.

---

# 10. Architectural Maturity

VectorEngine v1.5 demonstrates:

- Clean layering
- AI provider abstraction
- Resilient fallback
- Structured logging
- Deterministic local execution
- Production-ready composition

This is infrastructure-grade AI backend engineering.


