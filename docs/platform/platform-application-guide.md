# Cognitive Platform — Application Builder's Guide

## Purpose

How to use this platform's components when building any application on top of it.
This applies whether building an internal service, a domain application (e.g. UPSC Brain),
or any future consumer of the platform.

---

## AI Tool Usage Strategy

| Tool | Role | When to use |
|---|---|---|
| GitHub Copilot | Fast code generation | boilerplate, repetitive patterns, filling known structures |
| Claude Code | Architecture reasoning, refactoring, debugging | design decisions, complex refactors, unfamiliar code, root cause analysis |
| OpenAI APIs | LLM integration inside the platform | LLM calls made by platform services (generation, RAG, agent reasoning) |

---

## Always Start With Core

Every application built on this platform must use `core/` for foundational concerns.
Never reimplement these inside your application.

| Need | Use |
|---|---|
| Read config / environment | `core/config.settings` |
| Structured logging | `core/logging.logger` |
| Prometheus metrics | `core/metrics.metrics` |
| Postgres connection | `core/database.postgres` |
| Redis connection | `core/redis.redis` |

See [core/CLAUDE.md](../../core/CLAUDE.md) for usage patterns.

---

## Choosing the Right Platform Component

Use this as a decision guide when building any feature or application.

### Need to call an LLM?
→ Use **LLM Gateway** (Phase 4)
- All LLM calls must go through the gateway — never call providers directly from application code
- Gateway handles routing, caching, streaming, cost tracking
- Before Phase 4: direct LLM calls are acceptable as a temporary measure in POC work only

### Need to ingest, search, or retrieve documents?
→ Use **RAG Service** (Phase 5)
- Handles ingestion, chunking, embedding, vector search, context assembly
- Built on pgvector for local vector storage
- For early POC: call embeddings and pgvector directly via `core/database`

### Need an agent that reasons, plans, and uses tools?
→ Use **Agent Service** (Phase 6)
- Provides planning loop, memory, tool use, task execution
- Built on LangGraph
- For early POC: implement reasoning loop directly with LangGraph in your application

### Need ML model inference or LLM output evaluation?
→ Use **ML + Evaluation Service** (Phase 7)
- Feature engineering, model inference, LLM output evaluation and scoring
- For early POC: implement evaluator directly in application code

### Need async event processing or workflow orchestration?
→ Use **Event Runtime** (Phase 8)
- Append-only log, consumer groups, projection engine, workflow scheduler
- For early POC: use local async or direct function calls

### Need metrics and dashboards?
→ Use `core/metrics` + existing **Prometheus + Grafana** stack (Phase 2 — already running)
- Expose a `/metrics` endpoint in your FastAPI service
- Prometheus scrapes it automatically if added to `docker/observability/prometheus/prometheus-config.yml`

---

## Application Service Pattern

Every application service built on this platform should follow this structure:

```
your-service/
  main.py           # FastAPI app, startup, shutdown
  config.py         # service-specific config (extends core/config if needed)
  routes/           # API endpoints
  services/         # business logic
  models/           # data models / schemas
  tests/
    unit/
    integration/
```

At startup, always:
1. Load config via `core/config.settings`
2. Initialise logger via `core/logging.logger`
3. Connect to Postgres and Redis via `core/database` and `core/redis`
4. Expose `/health` and `/metrics` endpoints

---

## Integration Order for a New Application

Follow this order when integrating platform components into a new application:

1. **Start** — `core/` only (config, logging, metrics, db, redis)
2. **Add LLM calls** — direct calls first, replace with LLM Gateway when Phase 4 is ready
3. **Add RAG** — direct pgvector calls first, replace with RAG Service when Phase 5 is ready
4. **Add agents** — LangGraph directly first, replace with Agent Service when Phase 6 is ready
5. **Add ML/evaluation** — custom evaluator first, replace with ML+Eval Service when Phase 7 is ready
6. **Add async workflows** — local async first, replace with Event Runtime when Phase 8 is ready

This allows early POC work to proceed without waiting for all platform phases to complete.

---

## Before Starting Any New Application

- [ ] Check [platform-requirements.md](platform-requirements.md) — does this app align with a planned system?
- [ ] Check [platform-architecture.md](platform-architecture.md) — which layer does this app sit in?
- [ ] Check [platform-repo-structure.md](platform-repo-structure.md) — which folder does it start in?
- [ ] If this is an external application repo, add it to [platform-repo-structure.md — External Application Repos](platform-repo-structure.md#external-application-repos)
- [ ] Confirm `core/` modules are available and tested
- [ ] Confirm Docker infrastructure is running
