# Cognitive Platform — CLAUDE.md

## Purpose

Development guidelines for Claude Code. Answers **how to build** in this repo.
For **what to build** see [Platform Index](docs/platform/platform-index.md).

---

## Repo Context

- Monorepo. Components start here and graduate to separate repos when mature.
- No cloud. Everything runs locally via Docker.
- Do not create separate repos or build components ahead of their phase.

See [platform-repo-structure.md](docs/platform/platform-repo-structure.md) for the full folder map and graduation criteria.

---

## Build Order

Each system depends on the one before it — do not skip phases.

See [platform-architecture.md → System Build Dependency Graph](docs/platform/platform-architecture.md#system-build-dependency-graph).
See [phases-overview.md](docs/platform/phases/phases-overview.md) for phase status, stage breakdown, and runbook links.

**Active phase: Phase 3 — Mini GPT.** See [models/CLAUDE.md](models/CLAUDE.md).

---

## How to Start Work

```bash
source .venv/bin/activate
docker compose --env-file .env -f docker/cognitive-compose.yml up -d
docker compose --env-file .env -f docker/cognitive-compose.yml ps
PYTHONPATH=. .venv/bin/pytest tests/unit/ tests/integration/ -v
```

---

## How to Build a New Module

1. Check [platform-repo-structure.md](docs/platform/platform-repo-structure.md) — confirm the correct folder and phase
2. Create the module under the correct folder
3. Import shared infra from `core/` — never reimplement config, logging, metrics, db, or redis
4. Write unit tests in `tests/unit/<folder>/` — must run without containers
5. Write integration tests in `tests/integration/<folder>/` — if the module touches infra
6. Run both test suites before considering the module complete

---

## Core Module Imports

```python
from core.config.settings import settings          # typed config from .env
from core.logging.logger import logger             # structlog key=value pairs
from core.metrics.metrics import REQUEST_COUNT, REQUEST_LATENCY  # prometheus
from core.database.postgres import get_connection  # psycopg3 connection factory
from core.redis.redis import get_redis             # redis-py client factory
```

See [core/CLAUDE.md](core/CLAUDE.md) for full usage patterns and examples.

---

## How to Run Tests

```bash
# Unit tests — no containers needed
PYTHONPATH=. .venv/bin/pytest tests/unit/ -v

# Integration tests — containers must be running
PYTHONPATH=. .venv/bin/pytest tests/integration/ -v

# Smoke test core connectivity
PYTHONPATH=. .venv/bin/python scripts/test_core.py
```

---

## Infrastructure Reference

| Container | Port | Credentials |
|---|---|---|
| cognitive-postgres | 5432 | cognitive / cognitive |
| cognitive-redis | 6379 | — |
| cognitive-prometheus | 9090 | — |
| cognitive-grafana | 3000 | admin / admin |
| cognitive-postgres-exporter | 9187 | — |
| cognitive-redis-exporter | 9121 | — |

pgvector is enabled on cognitive-postgres.

```bash
docker compose -f docker/cognitive-compose.yml --env-file .env up -d
docker compose -f docker/cognitive-compose.yml --env-file .env down
docker compose -f docker/cognitive-compose.yml --env-file .env logs
```

`--env-file .env` is always required — the compose file lives in a subdirectory.

---

## Engineering Rules

- No notebooks. All work must be importable modules or runnable scripts.
- Tests are mandatory: unit (mocked) + integration (live infra) where applicable.
- Always set `PYTHONPATH=.` when running Python from the project root.
- Always use `--env-file .env` with docker compose.
- `.env` is gitignored — `.env.example` is the committed template.
- Never add config, logging, metrics, db, or redis logic inside a service — always use `core/`.
- Do not build inside `services/` or `infra/` before their phase begins.

---

## Docs

| Doc | Purpose |
|---|---|
| [Platform Index](docs/platform/platform-index.md) | All platform docs, phases, and component guides |
| [Examiner Brain Requirements](docs/application-validation/examiner-brain-requirements.md) | UPSC domain scope — platform validation |
| [core/CLAUDE.md](core/CLAUDE.md) | How to use shared core modules |
| [models/CLAUDE.md](models/CLAUDE.md) | Phase 3 Mini GPT build guide |
