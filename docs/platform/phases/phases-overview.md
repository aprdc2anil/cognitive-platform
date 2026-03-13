# Platform Phases — Overview

Single source of truth for what is being built in each phase and its current status.

For the dependency chain between phases see [platform-architecture.md — System Build Dependency Graph](../platform-architecture.md#system-build-dependency-graph).

---

## Phase Summary

| Phase | Scope | Status | Runbook |
|---|---|---|---|
| 1 | Developer Workstation — IDE, Python, Java | **Complete** | [phase1-environment-runbook.md](phase1-environment-runbook.md) |
| 2 | Platform Engineering — Docker, infra, observability, core modules | **Complete** | [phase2-environment-runbook.md](phase2-environment-runbook.md) |
| 3 | Mini GPT — transformer from scratch | **In Progress** | phase3-minigpt-runbook.md *(coming)* |
| 4 | LLM Gateway (Java) | Pending | phase4-llm-gateway-runbook.md *(coming)* |
| 5 | RAG Service (Python) | Pending | phase5-rag-service-runbook.md *(coming)* |
| 6 | Agent Service (Python) | Pending | phase6-agent-service-runbook.md *(coming)* |
| 7 | ML + Evaluation Service (Python) | Pending | phase7-ml-eval-service-runbook.md *(coming)* |
| 8 | Event Runtime (Java) | Pending | phase8-event-runtime-runbook.md *(coming)* |
| 9 | AI Copilot | Pending | phase9-copilot-runbook.md *(coming)* |

---

## Phase 1 — Developer Workstation

**Status: Complete**

Goal: Establish a developer workstation capable of building the Cognitive Platform.

| Stage | Scope | Status |
|---|---|---|
| 1 | Linux shell environment (WSL / macOS / native Linux) | Complete |
| 2 | Development workspace (`~/dev/git/cognitive-platform`) | Complete |
| 3 | Git repository — monorepo, GitHub remote | Complete |
| 4 | IDE + AI tools — VS Code, GitHub Copilot, Claude Code | Complete |
| 5 | Language runtimes — Python `.venv`, Java 21 | Complete |

---

## Phase 2 — Platform Engineering

**Status: Complete**

Goal: Docker, containerised infrastructure, observability, Python runtime, shared core modules.

| Stage | Scope | Status |
|---|---|---|
| 1 | Docker installation | Complete |
| 2 | Platform repository structure | Complete |
| 3 | Persistent storage volumes | Complete |
| 4 | Docker infrastructure stack — Postgres, Redis, Prometheus, Grafana | Complete |
| 5 | Observability — prometheus exporters, Grafana dashboards | Complete |
| 6 | Backup and recovery — WSL snapshot script | Complete |
| 7 | Python service runtime — packages in `.venv` | Complete |
| 8 | Docker Compose split — structured layout under `docker/` | Complete |
| 9 | Shared platform core — config, logging, metrics, database, redis | Complete |

---

## Phase 3 — Mini GPT

**Status: In Progress**

Goal: Implement a minimal transformer language model from scratch using PyTorch.
Trains locally on CPU. Dataset: Tiny Shakespeare.

Builds on: core modules (Phase 2).
Unlocks: foundational transformer and embedding knowledge needed before building LLM infrastructure.

| Stage | Scope | Status |
|---|---|---|
| 1 | `config.py` — hyperparameters as dataclass | Pending |
| 2 | `tokenizer.py` — character-level tokenizer | Pending |
| 3 | `embeddings.py` — token + positional embeddings | Pending |
| 4 | `attention.py` — single-head → multi-head attention | Pending |
| 5 | `transformer.py` — transformer block with residuals + layer norm | Pending |
| 6 | `model.py` — full GPT assembly | Pending |
| 7 | `train.py` — training loop, cross-entropy, AdamW | Pending |
| 8 | `sample.py` — autoregressive text generation | Pending |

See [models/CLAUDE.md](../../../models/CLAUDE.md) for implementation guide.

---

## Phase 4 — LLM Gateway

**Status: Pending**

Goal: Unified inference gateway routing to multiple LLM providers.
All LLM calls from every service above must go through this gateway.

Builds on: Phase 2 infrastructure (Redis for caching, Postgres for usage tracking).
Unlocks: RAG Service, Agent Service, ML+Eval Service (all require LLM calls).

| Stage | Scope | Status |
|---|---|---|
| 1 | Spring Boot / Netty project setup | Pending |
| 2 | Provider adapters (OpenAI, Anthropic) | Pending |
| 3 | Model routing | Pending |
| 4 | Token streaming | Pending |
| 5 | Request caching (Redis) | Pending |
| 6 | Usage tracking (Postgres) | Pending |

---

## Phase 5 — RAG Service

**Status: Pending**

Goal: Document ingestion, embedding, vector search, and retrieval-augmented generation.
First Python AI service — builds the retrieval layer that all agents and tools depend on.

Builds on: LLM Gateway (Phase 4) for generation, pgvector (Phase 2) for vector storage.
Unlocks: Agent Service (Phase 6) — agents need retrieval to be useful.

| Stage | Scope | Status |
|---|---|---|
| 1 | Document ingestion — PDF, text, web | Pending |
| 2 | Chunking + embedding pipeline | Pending |
| 3 | Pluggable vector backend (pgvector default) | Pending |
| 4 | Context assembly | Pending |
| 5 | Generation via LLM Gateway | Pending |
| 6 | `/ingest`, `/search`, `/query` API endpoints | Pending |

---

## Phase 6 — Agent Service

**Status: Pending**

Goal: Stateful agent reasoning loop with planning, memory, tool use, and task execution.

Builds on: LLM Gateway (Phase 4) for reasoning, RAG Service (Phase 5) for context retrieval.
Unlocks: ML + Evaluation Service (Phase 7) — evaluates agent-generated content.

| Stage | Scope | Status |
|---|---|---|
| 1 | LangGraph project setup | Pending |
| 2 | Planning loop (think → act → observe cycle) | Pending |
| 3 | Memory — short-term (session) + long-term (Postgres) | Pending |
| 4 | Tool use — RAG retrieval, LLM calls, custom tools | Pending |
| 5 | Task execution — multi-step task decomposition | Pending |
| 6 | `/run`, `/status`, `/history` API endpoints | Pending |

---

## Phase 7 — ML + Evaluation Service

**Status: Pending**

Goal: Feature engineering, model inference, and LLM output evaluation and scoring.
Provides quality assessment for agent outputs, RAG results, and LLM responses.

Builds on: LLM Gateway (Phase 4) for scoring calls, Agent Service (Phase 6) for content to evaluate.
Unlocks: Event Runtime (Phase 8) — production async upgrade for all Python services.

| Stage | Scope | Status |
|---|---|---|
| 1 | Feature engineering pipeline | Pending |
| 2 | Model inference service | Pending |
| 3 | LLM output evaluation — quality, relevance, factuality | Pending |
| 4 | Confidence scoring | Pending |
| 5 | Answer evaluation — correctness, completeness | Pending |
| 6 | `/evaluate`, `/score`, `/predict` API endpoints | Pending |

---

## Phase 8 — Event Runtime

**Status: Pending**

Goal: Async backbone — upgrades all Python AI services (Phases 5–7) with production-grade event-driven data flow.
Built after the services it powers so the async upgrade is driven by real service needs.

Builds on: all Phase 5–7 services (provides their async event infrastructure).
Unlocks: AI Copilot (Phase 9) — copilot uses event-driven workflows for async tasks.

| Stage | Scope | Status |
|---|---|---|
| 1 | Java project setup | Pending |
| 2 | Append-only event log | Pending |
| 3 | Consumer groups | Pending |
| 4 | Projection engine | Pending |
| 5 | Workflow scheduler | Pending |
| 6 | Integration with RAG, Agent, ML+Eval services | Pending |

---

## Phase 9 — AI Copilot

**Status: Pending**

Goal: Developer productivity assistant built on the full platform stack.

Builds on: all platform services — LLM Gateway, RAG Service, Agent Service, Event Runtime.

| Stage | Scope | Status |
|---|---|---|
| 1 | FastAPI service setup | Pending |
| 2 | PR summary feature | Pending |
| 3 | Code explanation feature | Pending |
| 4 | Test generation feature | Pending |
| 5 | Refactor suggestions feature | Pending |
