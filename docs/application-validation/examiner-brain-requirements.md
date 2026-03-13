# Examiner Brain — Domain Requirements

## Overview

UPSC-domain-specific requirements for the Examiner Brain and Trainer Brain.
This document lives in `cognitive-platform` for platform validation only.
The implementation repo is `upsc-agent` (separate, not yet created).

For platform components see [platform-application-guide.md](../platform/platform-application-guide.md).
For platform phases see [phases-overview.md](../platform/phases/phases-overview.md).
For generic platform scope see [platform-requirements.md](../platform/platform-requirements.md).

---

## Objectives

**Objective 1 — Examiner Brain (Iteration 1 + 2)**
Simulate real UPSC examiner behaviour to generate realistic exams from syllabus, past papers,
and recent current affairs events.
- Iteration 1: Autonomous PDF generation (POC)
- Iteration 2: Interactive UI-based assessment and performance tracking

**Objective 2 — Trainer Brain (Iteration 2)**
Analyse candidate performance and drive adaptive learning:
- mastery tracking, learning task generation, resource recommendation, targeted practice

**Objective 3 — Reusable cognitive infrastructure libraries**
ConceptGraph, ConceptKV, AdaptiveMasteryEngine — domain-independent, open-source.

**Objective 4 — Agentic RAG and distributed infra stack**
Learn and implement: LangGraph, LangChain, LlamaIndex, Chroma, Kafka, Spark,
Cassandra, Redis, Temporal, Airflow, Iceberg, Kubernetes.

**Objective 5 — GenAI-accelerated development within cost constraints**
Production deployment cost < **$300/month**.

---

## Iteration Definitions

Product milestones — what gets delivered, not how it is built.

### Iteration 1 — Autonomous PDF Generation (POC)

Mode: Fully autonomous. No UI. No user interaction.
Purpose: Validate the end-to-end cognitive question generation pipeline.

Pipeline:
- selects concepts from ConceptGraph
- links recent events to historical concepts via activation propagation
- generates questions with confidence scores via LLM
- produces reasoning traces
- renders output as PDFs

Outputs: Question Paper PDF, Answer Key PDF, Explanation PDF, Examiner Reasoning PDF

### Iteration 2 — Interactive Assessment + Trainer Brain

Mode: Interactive UI + async workflows.

Examiner Brain:
- generate question papers dynamically
- present questions in UI
- accept candidate answers, evaluate, compute scores
- store and track candidate performance

Trainer Brain (activates after each assessment):
- analyse performance, identify weak concepts
- update mastery state in ConceptKV
- generate learning tasks, recommend resources
- generate targeted practice questions
- track progression over time

---

## Platform Component Map

Every examiner brain capability maps to a `cognitive-platform` phase.
Build the platform phase first, then build the examiner brain capability on top.

| Examiner Brain Capability | Platform Component | Platform Phase | POC Path (before platform phase ready) |
|---|---|---|---|
| Knowledge graph + graph traversal (ConceptGraph) | Postgres graph patterns (adjacency + recursive CTE) | Phase 2 — done | Already available |
| Cognitive state store (ConceptKV) | core/redis | Phase 2 — done | Already available |
| Performance data persistence | core/database (Postgres) | Phase 2 — done | Already available |
| Observability | core/metrics + Prometheus + Grafana | Phase 2 — done | Already available |
| LLM calls (question gen, reasoning, evaluation) | LLM Gateway | Phase 4 | Direct LLM API calls |
| Document ingestion (syllabus, past papers, events) | RAG Service — ingestion pipeline | Phase 5 | Direct file parsing |
| Embedding + vector search (concept retrieval) | RAG Service — pgvector backend | Phase 5 | Direct pgvector via core/database |
| Agent reasoning loop (activation, concept selection) | Agent Service — LangGraph | Phase 6 | LangGraph directly in app |
| Confidence scoring / LLM output evaluation | ML + Evaluation Service | Phase 7 | Custom evaluator in app |
| Event-driven ingestion + async workflows | Event Runtime | Phase 8 | Local async / LangGraph state machine |

---

## UPSC Build Phases

How the examiner brain is built incrementally — each UPSC phase maps to a platform phase prerequisite.
UPSC Phase numbering is independent of platform phases (Platform Phase 1–9) and future project phases.

### UPSC Phase 1 — Cognitive Foundation
**Unlocked by: Platform Phase 2 (complete)**

Platform dependencies: `core/database`, `core/redis`, `core/metrics`, `core/logging`

Build:
- ConceptGraph schema in Postgres (node + edge tables, recursive CTE traversal, pgvector for semantic search)
- ConceptKV wrapper on `core/redis` (typed key-value access to cognitive state)
- Data ingestion — local file parsing (syllabus, past papers, current affairs)
- Activation engine — graph traversal and propagation via SQL
- Pattern engine — concept selection and threshold scoring logic

Delivers: cognitive infrastructure foundation — can run without any LLM calls.

---

### UPSC Phase 2 — Examiner Brain POC (Iteration 1 complete)
**Unlocked by: Platform Phase 3 (LLM familiarity) + Phase 4 (LLM Gateway)**

Platform dependencies: LLM Gateway (Phase 4)
POC path: direct LLM API calls while Phase 4 is pending

Build:
- Question generator — questions via LLM Gateway
- Confidence engine — custom evaluator (upgraded in UPSC Phase 5)
- Reasoning generator — examiner traces via LLM Gateway
- PDF generator — question paper, answer key, explanation, reasoning PDFs
- Full Iteration 1 pipeline: events → ConceptGraph activation → LLM question gen → PDF output

Delivers: **Iteration 1 complete** — autonomous end-to-end question paper generation.

---

### UPSC Phase 3 — RAG-backed Ingestion
**Unlocked by: Platform Phase 5 (RAG Service)**

Platform dependencies: RAG Service (Phase 5)
POC path: local file parsing (UPSC Phase 1) used until Phase 5 is ready

Upgrade:
- Replace local file parsing with RAG Service ingestion pipeline
- Syllabus, past papers, current events ingested via RAG Service
- Concept retrieval via RAG vector search (pgvector backend)
- ConceptGraph populated via concept extractor + semantic retrieval

Delivers: ingestion layer backed by platform RAG — scalable document pipeline.

---

### UPSC Phase 4 — Agent-driven Reasoning
**Unlocked by: Platform Phase 6 (Agent Service)**

Platform dependencies: Agent Service (Phase 6), RAG Service (Phase 5)
POC path: LangGraph directly in app until Phase 6 is ready

Upgrade:
- Replace direct LangGraph with Agent Service
- Activation propagation driven by agent planning loop
- Multi-step concept selection as agent task execution
- RAG-backed context retrieval as agent tool

Delivers: fully agent-driven, RAG-backed, LLM-Gateway-routed pipeline for Iteration 1.

---

### UPSC Phase 5 — Interactive Assessment + Trainer Brain (Iteration 2 complete)
**Unlocked by: Platform Phase 7 (ML + Evaluation Service)**

Platform dependencies: ML + Evaluation Service (Phase 7), Agent Service (Phase 6)
POC path: custom answer evaluator and custom confidence scoring until Phase 7 is ready

Build:
- Assessment session manager — live question paper presentation
- Answer evaluator — candidate answer scoring via ML + Evaluation Service
- Result computer — scoring pipeline
- Performance recorder — Postgres via `core/database`
- Trainer Brain:
  - Performance analyzer
  - Mastery updater (ConceptKV via `core/redis`)
  - Task generator + resource recommender
  - Practice question generator
  - Progress tracker (AdaptiveMasteryEngine)

Delivers: **Iteration 2 complete** — interactive assessment with Trainer Brain feedback loop.

---

### UPSC Phase 6 — Event-driven Workflows (Production-ready)
**Unlocked by: Platform Phase 8 (Event Runtime)**

Platform dependencies: Event Runtime (Phase 8)
POC path: local async used throughout UPSC Phases 1–5

Upgrade:
- Replace local async with Event Runtime throughout
- Event-driven current affairs ingestion (append-only event log)
- Async assessment session workflows (consumer groups)
- Async Trainer Brain task generation (projection engine)
- Full system event-driven and production-ready

Delivers: production-grade async backbone across all examiner brain + trainer brain workflows.

---

## Core Cognitive Architecture

### ConceptGraph

Knowledge graph storing concepts, relationships, events, and questions.

Supports: activation propagation, graph traversal, semantic retrieval.

**Implementation:** Postgres — adjacency model (node + edge tables), recursive CTE for traversal and activation propagation, pgvector for semantic retrieval. No separate graph DB required.

Reusable — domain independent.

### ConceptKV

State store for mastery state, activation scores, performance history, cached results.

**Implementation:** built on `core/redis`. ConceptKV is a typed wrapper — it organises keys and serialisation on top of Redis, it does not replace it.

Reusable — domain independent.

### AdaptiveMasteryEngine

Tracks mastery evolution. Generates personalised learning plans.
Drives Trainer Brain task generation.

Reusable — domain independent.

---

## Activation and Question Generation Pipeline

```
Recent Events
  → activate related concepts in ConceptGraph
  → propagate activation to related historical concepts
  → activate pattern memory
  → compute activation score per concept
  → compute confidence score
  → generate question if score exceeds threshold
  → attach reasoning trace to question
```

---

## Examiner Brain Modules

### Core modules (both iterations)

| Module | Responsibility | Platform dependency |
|---|---|---|
| `event_ingestor.py` | ingest current affairs events | RAG Service (Phase 5) / local file (UPSC Phase 1) |
| `activation_engine.py` | activation propagation over ConceptGraph | core/database (Phase 2) |
| `pattern_engine.py` | detect question-worthy patterns | core/database (Phase 2) |
| `concept_selector.py` | select concepts above threshold | core/database (Phase 2) |
| `question_generator.py` | generate questions via LLM | LLM Gateway (Phase 4) |
| `confidence_engine.py` | score question quality and confidence | ML + Eval Service (Phase 7) / custom (UPSC Phase 2) |
| `reasoning_generator.py` | generate examiner reasoning trace | LLM Gateway (Phase 4) |

### Iteration 1 only

| Module | Responsibility | Platform dependency |
|---|---|---|
| `pdf_generator.py` | render question paper, answer key, explanation, reasoning PDFs | None (app-level) |

### Iteration 2 only

| Module | Responsibility | Platform dependency |
|---|---|---|
| `assessment_session_manager.py` | manage live assessment sessions | Event Runtime (Phase 8) / local async |
| `answer_evaluator.py` | evaluate candidate answers | ML + Eval Service (Phase 7) |
| `result_computer.py` | compute scores | core/database (Phase 2) |
| `performance_recorder.py` | persist performance data | core/database (Phase 2) |

---

## Trainer Brain Modules

| Module | Responsibility | Platform dependency |
|---|---|---|
| `performance_analyzer.py` | analyse assessment results | ML + Eval Service (Phase 7) |
| `mastery_updater.py` | update ConceptKV mastery state | core/redis (Phase 2) |
| `task_generator.py` | generate learning tasks | Agent Service (Phase 6) |
| `resource_recommender.py` | recommend study resources | RAG Service (Phase 5) |
| `practice_question_generator.py` | generate targeted practice questions | LLM Gateway (Phase 4) |
| `progress_tracker.py` | track learning progression | core/database (Phase 2) |

---

## Data Ingestion Layer

| Module | Responsibility | Platform dependency |
|---|---|---|
| `syllabus_ingestor.py` | parse and ingest UPSC syllabus | RAG Service (Phase 5) / local file (UPSC Phase 1) |
| `past_paper_ingestor.py` | ingest past exam papers | RAG Service (Phase 5) / local file (UPSC Phase 1) |
| `event_ingestor.py` | ingest current affairs events | RAG Service (Phase 5) / Event Runtime (Phase 8) |
| `concept_extractor.py` | extract concepts and relationships for ConceptGraph | LLM Gateway (Phase 4) |

---

## Technology Stack

### Platform Layer (provided by cognitive-platform)

See [platform-tech-stack.md](../platform/platform-tech-stack.md) for the full platform stack.

Platform components consumed: `core/database`, `core/redis`, `core/metrics`, `core/logging`, LLM Gateway, RAG Service, Agent Service, ML + Evaluation Service, Event Runtime, Prometheus + Grafana + structlog.

### Examiner Brain Additions (upsc-agent repo only)

| Layer | UPSC Phase 1–2 (POC) | UPSC Phase 3–5 (Iteration 2) | UPSC Phase 6 (Production) |
|---|---|---|---|
| ConceptGraph | Postgres adjacency model | Postgres adjacency model | Postgres + Cassandra (scale) |
| ConceptKV | Redis (core/redis) | Redis (core/redis) | Redis + Cassandra (scale) |
| Vector backend | pgvector (platform) | pgvector (platform) | Chroma cluster / Milvus |
| Messaging | local async | Event Runtime (Phase 8) | Kafka |
| Batch processing | Python batch | Python batch | Spark |
| Workflow DAG | LangGraph direct | Agent Service + Event Runtime | Temporal + Airflow |
| LLM evaluation | custom evaluator | ML + Eval Service (Phase 7) | LangSmith / DeepEval |

---

## Production Scaling Tiers

Tier 1 infrastructure is fully covered by the `cognitive-platform` Docker stack (already running).

| Tier | What Gets Added | Type |
|---|---|---|
| 1 | Postgres + pgvector + Redis — cognitive-platform stack | Platform (done) |
| 2 | Kafka — high-throughput event streaming | External |
| 3 | Temporal + Airflow — durable workflows + scheduling | External |
| 4 | Cassandra + Spark + Iceberg — graph scale, batch, data lake | External |
| 5 | Kubernetes — fully distributed | External |

---

## Deployment

### Initial — Single VM (reuses cognitive-platform Docker stack)

```
cognitive-platform docker stack (already running)
  ├── Postgres + pgvector  → ConceptGraph + vector search
  ├── Redis                → ConceptKV
  └── Prometheus + Grafana → observability

upsc-agent services (added on top)
  ├── FastAPI              → API layer
  ├── LangGraph            → agent reasoning (UPSC Phase 2+, replaced by Agent Service at UPSC Phase 4+)
  └── platform services    → LLM Gateway, RAG Service, Agent Service, Event Runtime
```

Cost target: < $300/month

### Future — Kubernetes

```
Kubernetes
  ├── Examiner Brain services
  ├── Trainer Brain services
  ├── ConceptGraph services
  └── Kafka, Spark, Cassandra, Redis
```

---

## Repository Structure (upsc-agent repo)

```
upsc-agent/
  apps/api/
  libs/
    conceptgraph/
    conceptkv/
    mastery_engine/
  examiner_brain/
  trainer_brain/
  ingestion/
  evaluation/
  tools/
  configs/
  datasets/
  infra/
  docs/
```

---

## Cost Constraints

- Self-host vector DB (pgvector default, Chroma only when needed)
- Use local embeddings (sentence-transformers) until scale requires HuggingFace hosted
- Avoid managed services initially
- Cache aggressively (ConceptKV on Redis)

---

## Success Criteria

- Examiner Brain generates realistic UPSC-style exam papers
- Questions linked to recent events with explainable reasoning traces
- Trainer Brain drives measurable improvement in weak areas
- Deployment cost < $300/month
- ConceptGraph, ConceptKV, AdaptiveMasteryEngine reusable across domains
- System scalable from single-node Docker to Kubernetes
- All output is explainable

---

## Current Status

**Not started.** Implementation is in `upsc-agent` repo (separate, not yet created).

### UPSC Phase Readiness

| UPSC Phase | Platform Prerequisite | Status |
|---|---|---|
| UPSC Phase 1 — Cognitive Foundation | Platform Phase 2 | **Ready to start** |
| UPSC Phase 2 — Examiner Brain POC (Iteration 1) | Platform Phase 4 (LLM Gateway) | Blocked — Phase 4 pending |
| UPSC Phase 3 — RAG-backed Ingestion | Platform Phase 5 (RAG Service) | Blocked — Phase 5 pending |
| UPSC Phase 4 — Agent-driven Reasoning | Platform Phase 6 (Agent Service) | Blocked — Phase 6 pending |
| UPSC Phase 5 — Interactive Assessment + Trainer Brain (Iteration 2) | Platform Phase 7 (ML + Eval Service) | Blocked — Phase 7 pending |
| UPSC Phase 6 — Event-driven Workflows (production-ready) | Platform Phase 8 (Event Runtime) | Blocked — Phase 8 pending |

### Day 1 tasks (when creating upsc-agent repo)

UPSC Phase 1 can begin immediately — no additional platform work needed:
- `upsc-agent` repo setup
- ConceptGraph schema in Postgres (node + edge tables, pgvector column)
- ConceptKV wrapper on `core/redis`
- Activation engine (SQL recursive CTE)
- Local file ingestion (syllabus, past papers)
