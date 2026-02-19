# ENGINEERING_DECISIONS.md

# VectorEngine — Engineering Decisions Log

**Version:** 1.5

This document records deliberate architectural and technical decisions (ADRs) made during the development of VectorEngine.

---

# ADR-001: Clean Architecture Enforcement

**Decision:**  
Strict separation between domain, application, infrastructure, and API layers.

**Rationale:**  
Prevents AI-provider lock-in and infrastructure coupling.

**Impact:**  
Higher initial complexity, long-term replaceability.

---

# ADR-002: Embedding Dimension Fixed to 384

**Decision:**  
Use `all-MiniLM-L6-v2` embeddings (384-dim).

**Rationale:**  
Efficient tradeoff between quality and performance.

**Impact:**  
Changing the embedding model requires full re-indexing of stored vectors.

---

# ADR-003: pgvector as Initial Vector Store

**Decision:**  
Use PostgreSQL + pgvector.

**Rationale:**  
- Single database system
- Operational simplicity
- ANN-ready

**Impact:**  
Scales vertically first. Horizontal scaling deferred.

---

# ADR-004: Deterministic Local LLM Adapter

**Decision:**  
Implement `LocalAdapter` for development and fallback.

**Rationale:**  
- Avoid hard dependency on paid APIs
- Enable deterministic CI testing
- Guarantee system stability under quota failure

**Impact:**  
Fallback responses are non-semantic but structurally valid.

---

# ADR-005: Fallback Strategy in Orchestrator

**Decision:**  
Fallback implemented at orchestration layer, not API layer.

**Rationale:**  
Keeps resilience inside AI execution boundary.  
Avoids HTTP layer contamination.

**Impact:**  
System degrades gracefully without breaking contracts.

---

# ADR-006: Structured Logging with request_id

**Decision:**  
Inject UUID per request and propagate via logs.

**Rationale:**  
- Traceability across layers
- Latency diagnostics
- Future compatibility with distributed tracing systems

**Impact:**  
Minimal overhead, major debugging benefit.

---

# ADR-007: Synchronous Execution (Phase 1.5)

**Decision:**  
Keep LLM execution synchronous.

**Rationale:**  
- Reduce concurrency complexity
- Simplify deterministic behavior

**Impact:**  
Throughput limited by single request execution.  
Async reserved for Phase 2.

---

# ADR-008: No External Orchestration Framework

**Decision:**  
Avoid LangChain, CrewAI, LlamaIndex.

**Rationale:**  
- Full control over orchestration logic
- Avoid unnecessary abstraction layers
- Maintain architectural transparency

**Impact:**  
More custom code.  
Higher clarity.

---

# ADR-009: Generic Stable Matching Engine (Phase 2)

**Decision:**  
Implement a lightweight Gale–Shapley stable matching engine inside VectorEngine and expose it via:

```
POST /matching/run
```

This engine is domain-agnostic and will be reusable across services such as:

- Financial Document Analyst (e.g., matching portfolios ↔ risk profiles, analysts ↔ cases)
- CV Maker Service (e.g., candidates ↔ job requirements, skills ↔ role priorities)

**Input (Generic Form):**  
- Group A entities with ordered preferences  
- Group B entities with ordered preferences

**Output:**  
- Stable allocation (no blocking pairs)

**Rationale:**  
- Demonstrates deterministic algorithmic capability beyond RAG  
- Aligns with allocation / optimization systems (including Tether-like platforms)  
- Keeps engine reusable across multiple verticals (finance, recruitment, education)

**Impact:**  
- +10% architectural signal strength (algorithmic credibility)  
- Expands system scope from AI orchestration to decision engine capability  
- Maintains clean separation (pure application-layer service, no infrastructure coupling)

---

# ADR-010: Streaming Token Endpoint (Phase 2)

**Decision:**  
Add streaming response support using FastAPI async generators to simulate token-by-token LLM output.

Example endpoint:

```
GET /analysis/stream
```

**Implementation Strategy:**  
- Async generator in FastAPI  
- Yield incremental tokens  
- Optional simulation mode for deterministic CI

**Rationale:**  
- Demonstrates production-grade UX patterns  
- Aligns with modern LLM interaction models  
- Prepares system for real streaming providers

**Impact:**  
- +5–8% production-readiness signal  
- Enables progressive rendering UX  
- Introduces controlled async complexity (contained to API + orchestrator boundary)

---

# Future Considerations (Phase 2)

**Decision:**  
Add streaming response support using FastAPI async generators to simulate token-by-token LLM output.

Example endpoint:

```
GET /analysis/stream
```

**Implementation Strategy:**  
- Async generator in FastAPI  
- Yield incremental tokens  
- Optional simulation mode for deterministic CI

**Rationale:**  
- Demonstrates production-grade UX patterns  
- Aligns with modern LLM interaction models  
- Prepares system for real streaming providers

**Impact:**  
- +5–8% production-readiness signal  
- Enables progressive rendering UX  
- Increases concurrency complexity (managed in Phase 2)

---

# Future Considerations (Phase 2)

- Circuit breaker pattern
- Token usage logging
- Caching layer (Redis)
- Async LLM execution
- Streaming responses
- Metrics exporter
- Horizontal scaling

---

# Engineering Intent

VectorEngine is not a demo.

It is an AI infrastructure core designed for:

- Financial analysis systems
- CV tailoring engines
- Knowledge retrieval platforms
- Decision-support systems

Every decision prioritizes replaceability, resilience, and architectural clarity.


