# Platform Technology Stack

Authoritative reference for all technologies used across the platform.
Inline "Stack:" notes in system descriptions reference this file for detail.

---

## Languages

| Language | Role | Constraint |
|---|---|---|
| Python | All AI services, ML, RAG, agents, data pipelines | Primary language |
| Java | LLM Gateway (Phase 4), Event Runtime (Phase 8) | Gateway + runtime layer |
| Go / Rust | Performance-critical components only | Use only if Python/Java are insufficient |

---

## Infrastructure

| Component | Role | Phase available |
|---|---|---|
| Docker + Docker Compose | All infrastructure containerised — no cloud required | Phase 2 |
| Postgres | Relational data store — primary database | Phase 2 |
| pgvector | Vector extension on Postgres — default vector backend | Phase 2 |
| Redis | State store, caching, pub/sub | Phase 2 |

---

## ML + AI

| Component | Role | Phase available |
|---|---|---|
| PyTorch | Model training — MiniGPT, custom models | Phase 3 |
| HuggingFace | Model hub, tokenizers, pretrained embeddings | Phase 3+ |
| LangChain | RAG pipeline construction | Phase 5 |
| LangGraph | Agent orchestration, stateful reasoning loops | Phase 6 |
| MLflow | Experiment tracking, model registry | Phase 7 |

---

## Vector Backends (pluggable)

RAG Service uses a pluggable vector backend. Default is pgvector (already in platform).
Swap to Chroma or Milvus when scale or isolation requires it.

| Backend | When to use |
|---|---|
| pgvector | Default — local, no extra service, already running |
| Chroma | When applications need a dedicated vector DB (self-hosted) |
| Milvus | Production-scale distributed vector search |

---

## Observability

| Component | Role | Phase available |
|---|---|---|
| Prometheus | Metrics collection, scraping, alerting rules | Phase 2 |
| Grafana | Dashboards — infrastructure and service metrics | Phase 2 |
| structlog | Structured logging (JSON key-value) — all Python services | Phase 2 |
| postgres-exporter | Postgres metrics → Prometheus | Phase 2 |
| redis-exporter | Redis metrics → Prometheus | Phase 2 |

---

## Python Service Runtime

| Package | Role |
|---|---|
| FastAPI + uvicorn | HTTP service framework |
| psycopg (psycopg3) | Postgres client |
| redis-py | Redis client |
| pydantic + pydantic-settings | Data validation + typed settings from `.env` |
| prometheus-client | Expose `/metrics` endpoint |
| pytest + pytest-asyncio | Test framework |
| black + ruff | Code formatting + linting |

---

## Java Runtime

| Package | Role |
|---|---|
| Spring Boot / Netty | HTTP service framework (LLM Gateway) |
| Maven / Gradle | Build tooling |
| Java 21 | Runtime — LTS version |

---

## External Technologies (application-level, not built by platform)

These are used by consumer applications (e.g. `upsc-agent`) at production scale.
The platform does not implement or manage them.

| Technology | Purpose | When added |
|---|---|---|
| Kafka | High-throughput event streaming | Production messaging |
| Temporal | Durable workflow execution | Production workflow DAGs |
| Airflow | Batch scheduling | Production scheduling |
| Cassandra | Wide-column store for large-scale state | Graph / state at scale |
| Spark | Distributed batch processing | Large-scale data pipelines |
| Iceberg | Data lake table format | Data lake storage |
| Kubernetes | Container orchestration | Production deployment |
| LangSmith / DeepEval | LLM evaluation tooling | Production evaluation |
