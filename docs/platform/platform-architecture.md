# Cognitive Platform — Architecture

## Operating Environment

- Linux or macOS (Windows users: see Phase 1 runbook for setup)
- Docker containers for all infrastructure
- Local only — no cloud required
- Python `.venv` for all Python work

---

## Technology Stack

See [platform-tech-stack.md](platform-tech-stack.md) for the full authoritative stack reference.

---

## Platform Architecture

```
Python AI Services
  ├── RAG Service          — ingestion, embeddings, vector search, generation
  ├── Agent Service        — planning loop, memory, tool use, task execution
  ├── ML + Eval Service    — feature engineering, inference, LLM scoring
  └── Copilot Service      — developer assistant (PR summaries, code explain, test gen)
        ↓ LLM calls                    ↓ async events
  Java LLM Gateway              Event Runtime (Java)
  ├── model routing              ├── append-only event log
  ├── provider adapters          ├── consumer groups
  ├── token streaming            ├── projection engine
  ├── request caching            └── workflow scheduler
  └── usage tracking
        ↓                               ↓
              Data Infrastructure
              ├── Postgres + pgvector (relational + default vector store)
              ├── Redis (state, caching, pub/sub)
              └── Graph patterns via Postgres (adjacency model + recursive CTE)
```

LLM Gateway and Event Runtime are parallel infrastructure services — both used by Python AI services, both backed by Data Infrastructure.

---

## Core Capability Domains

### Distributed Systems
- write-ahead logs, log-structured storage
- event sourcing, consumer groups
- workflow orchestration, stream processing
- Kafka, Redis Streams, Temporal (conceptual study)

### Generative AI Systems
- transformers, prompt engineering
- retrieval-augmented generation
- agent reasoning loops, tool use
- LLM output evaluation, confidence scoring, answer quality assessment

### ML Systems Engineering
- training pipelines, dataset management
- feature pipelines, experiment tracking
- model evaluation, inference services

### Platform Engineering
- service architecture, containerised deployment
- CI/CD pipelines, observability, API gateways

---

## System Build Dependency Graph

Systems must be built in order — this is a dependency chain, not just a sequence.

```
Platform Engineering (Phase 2)
         ↓
    Mini GPT (Phase 3)
         ↓
  LLM Gateway (Phase 4)
         ↓
   RAG Service (Phase 5)
         ↓
  Agent Service (Phase 6)
         ↓
ML + Eval Service (Phase 7)
         ↓
  Event Runtime (Phase 8)
         ↓
    AI Copilot (Phase 9)
```

- **Mini GPT** — builds on core modules; establishes transformer and embedding foundations
- **LLM Gateway** — routes all LLM calls; prerequisite for every service that generates or evaluates text
- **RAG Service** — depends on LLM Gateway for generation, pgvector (Phase 2) for retrieval
- **Agent Service** — depends on LLM Gateway for reasoning, RAG Service for retrieval context
- **ML + Eval Service** — depends on LLM Gateway for scoring calls; evaluates outputs from RAG and Agent services
- **Event Runtime** — built after the Python services it will power; upgrades them with production-grade async event flow
- **AI Copilot** — depends on the full stack: LLM Gateway, RAG, Agent, Event Runtime

---

## Graph Data Patterns

The platform supports graph-structured knowledge without a dedicated graph database.
Use Postgres with an adjacency model (node + edge tables) and recursive CTE queries for:
- concept relationship graphs (knowledge graphs)
- activation propagation over graph edges
- hierarchical and relational traversal

This covers ConceptGraph-style use cases on top of the existing Postgres infrastructure.
For production-scale graph workloads (billions of edges), a dedicated graph DB (Neo4j, JanusGraph) can be added as an external dependency — platform does not build or manage it.

---

## External Application Validation

Platform generality is validated by consumer applications built in separate repos.
These applications must be buildable using platform components with minimal custom infrastructure.

See [application-validation/platform-validation-index.md](../application-validation/platform-validation-index.md) for the list of validation applications and their platform component mappings.
