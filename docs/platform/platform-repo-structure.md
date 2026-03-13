# Cognitive Platform — Repository Structure

## Monorepo Strategy

`cognitive-platform` is the monorepo. All components start here.
Each component graduates to its own repo when it is mature enough to stand alone.
Do not create separate repos prematurely.

---

## Folder Map

| Folder | Purpose | Phase |
|---|---|---|
| `core/` | shared modules — permanent (config, logging, metrics, db, redis) | done |
| `models/` | ML model implementations — parent for all model work | done |
| `models/mini-gpt/` | transformer from scratch (PyTorch) | Phase 3 — active |
| `infra/llm-gateway/` | LLM gateway (Java) — placeholder | Phase 4 |
| `services/rag-service/` | RAG pipeline — placeholder | Phase 5 |
| `services/agent-service/` | agent orchestration — placeholder | Phase 6 |
| `services/ml-service/` | ML + evaluation service — placeholder | Phase 7 |
| `infra/event-runtime/` | event runtime (Java) — placeholder | Phase 8 |
| `services/copilot-service/` | developer assistant — placeholder | Phase 9 |
| `datasets/` | training datasets | as needed |
| `docker/` | infrastructure stack — permanent | done |
| `scripts/` | utility and smoke-test scripts — permanent | done |
| `tests/unit/` | unit tests — no containers required | done |
| `tests/integration/` | integration tests — live containers required | done |
| `docs/` | platform docs — permanent | done |

`infra/` and `services/` subdirectories are placeholders — do not build inside them until their phase begins.

---

## Repository Ecosystem

| Repo | Purpose | Graduates from |
|---|---|---|
| `cognitive-platform` | monorepo — stays as integration hub | — |
| `cognitive-llm` | transformer / MiniGPT experiments | `models/mini-gpt/` |
| `cognitive-gateway` | LLM inference gateway | `infra/llm-gateway/` |
| `cognitive-runtime` | event runtime / workflow engine | `infra/event-runtime/` |
| `cognitive-rag` | RAG platform | `services/rag-service/` |
| `cognitive-agents` | agent orchestration | `services/agent-service/` |
| `cognitive-ml` | ML pipelines and models | `services/ml-service/` |
| `cognitive-copilot` | developer AI assistant | `services/copilot-service/` |
| `cognitive-observability` | monitoring / metrics / tracing | stays in platform or separate |
| `cognitive-datasets` | shared datasets | `datasets/` |

---

## External Application Repos

These repos consume the platform. They are not part of the monorepo.
They validate that platform components are generic and reusable.

See [application-validation/platform-validation-index.md](../application-validation/platform-validation-index.md) for the full list of external application repos and their platform dependencies.

---

## Graduation Criteria

A component is ready to graduate when it:
- has a stable API
- has full unit and integration test coverage
- has its own Docker setup
- has no tight coupling to other in-progress components
- has its own runbook / documentation
