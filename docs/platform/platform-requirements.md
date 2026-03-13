# Cognitive Platform — Requirements

## Goal

Develop capability as an AI Systems Engineer capable of designing and implementing
production-style AI infrastructure including LLM platforms, ML pipelines, distributed
runtime systems, and scalable service architectures.

All systems must be implemented as deployable services — not notebooks, not toy demos.

---

## Focus Areas

- Distributed system design
- ML systems engineering
- LLM platform infrastructure
- RAG systems
- Agent systems
- Production service architecture

---

## Systems to Build

### 1 — Mini GPT
Minimal transformer language model from scratch.
- tokenizer, embeddings, transformer blocks, training loop, sampling
- Stack: Python, PyTorch
- Dataset: Tiny Shakespeare
- Learning focus: transformer architecture, training mechanics, attention mechanism

### 2 — LLM Gateway
Unified inference gateway routing to multiple LLM providers.
- model routing, provider adapters, streaming, caching, usage tracking
- Stack: Java, Spring Boot / Netty, Redis, Postgres
- Learning focus: service gateways, LLM orchestration, cost monitoring

### 3 — RAG Service
Document ingestion, embedding, vector search, and retrieval-augmented generation.
- document ingestion (PDF, text, web), chunking, embeddings, pluggable vector backend (pgvector default, Chroma / Milvus for scale), context assembly, generation
- Stack: Python, LangChain, pgvector
- Learning focus: enterprise RAG, vector search, document pipelines

### 4 — Agent Service
Stateful agent reasoning loop with planning, memory, tool use, and task execution.
- planning loop, memory (session + persistent), tool use, task decomposition, RAG integration
- Stack: Python, LangGraph
- Learning focus: agent systems, stateful reasoning, tool-augmented LLMs

### 5 — ML + Evaluation Service
Feature engineering, model inference, and LLM output evaluation.
- feature engineering, model inference, LLM output evaluation and scoring, confidence assessment
- Stack: Python, MLflow, FastAPI
- Learning focus: ML inference services, LLM evaluation, quality scoring

### 6 — Event Runtime
Lightweight distributed runtime on append-only event logs.
Upgrades Python AI services (RAG, Agent, ML+Eval) with production-grade async data flow.
- append-only log, consumer groups, projection runtime, workflow scheduler
- Stack: Java
- Learning focus: event sourcing, log-structured systems, workflow orchestration

### 7 — AI Copilot
Developer productivity assistant built on the full platform stack.
- PR summaries, code explanation, test generation, refactor suggestions
- Stack: Python, FastAPI, Redis, Postgres
- Learning focus: prompt engineering, developer tooling, LLM integration

---

## Development Phases

See [phases-overview.md](phases/phases-overview.md) — phase status, stage breakdown, and runbook links.

---

## Engineering Principles

**Prioritise:**
- production architecture
- modular services
- observability and testability
- scalable pipelines

**Avoid:**
- notebook-only experiments
- single-script ML pipelines
- toy demos

**Prefer:**
- service-based architecture
- event-driven design
- containerised deployment
