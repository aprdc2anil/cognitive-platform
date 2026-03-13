# Phase 2 — Platform Engineering Infrastructure

## Goal

Install Docker, build the containerised infrastructure stack, configure observability,
set up persistent storage, install the Python service runtime, and implement shared
platform core modules. This phase makes the environment ready to run all future services.

---

## Status

**Complete**

---

## Architecture

```
Linux
│
└── Docker
    │
    ├── Infrastructure Containers
    │   ├── Postgres + pgvector   :5432
    │   ├── Redis                 :6379
    │   ├── Prometheus            :9090
    │   └── Grafana               :3000
    │
    ├── Exporters
    │   ├── postgres-exporter     :9187
    │   └── redis-exporter        :9121
    │
    └── Network: cognitive-network

Python Runtime (.venv)
    ├── FastAPI + uvicorn
    ├── psycopg (Postgres client)
    ├── redis-py
    ├── prometheus-client
    └── structlog

Shared Core Modules
    core/config, core/logging, core/metrics, core/database, core/redis

Persistent Storage
    /var/lib/data/volumes/cognitive-platform/{postgres,redis,prometheus,grafana}
```

---

## Stages

### Stage 1 — Docker Installation
Status: Complete

Install Docker Engine. Allow current user to run Docker without sudo.

### Stage 2 — Platform Repository Structure
Status: Complete

Monorepo layout established:
```
cognitive-platform/
  core/ services/ infra/ models/ datasets/ docker/ scripts/ docs/
```
Service placeholders: `services/{rag,agent,ml,copilot}-service`
Infra placeholders: `infra/{llm-gateway,event-runtime}`

### Stage 3 — Persistent Storage
Status: Complete

```
/var/lib/data/volumes/cognitive-platform/
  postgres/  redis/  prometheus/  grafana/
```

### Stage 4 — Docker Infrastructure Stack
Status: Complete

Initial docker-compose with Postgres, Redis, Prometheus, Grafana on `cognitive-network`.
All containers use `json-file` log driver (max-size: 10m, max-file: 3).

### Stage 5 — Observability Stack
Status: Complete

Prometheus scrapes metrics every 15s.
Exporters: postgres-exporter (:9187), redis-exporter (:9121).
Grafana dashboards accessible at http://localhost:3000.

### Stage 6 — Backup and Recovery
Status: Complete

WSL snapshot backup via PowerShell script.
Script: `scripts/wslsnapshotscript.ps1`
Destination: `C:\GDrive\dev\wsl-backups\ubuntu`
Retains last 2 snapshots.

### Stage 7 — Python Service Runtime
Status: Complete

Packages installed in `.venv`:
```
fastapi  uvicorn  prometheus-client  psycopg[binary]  redis
pydantic  pydantic-settings  structlog
pytest  httpx  black  ruff
```

### Stage 8 — Docker Compose Split
Status: Complete

docker-compose split into structured layout:
```
docker/
  cognitive-compose.yml       # main entrypoint
  infra/
    postgres.yml
    redis.yml
  observability/
    prometheus-service.yml
    grafana.yml
    prometheus/
      prometheus-config.yml
```

Always run with:
```bash
docker compose -f docker/cognitive-compose.yml --env-file .env up -d
```

`--env-file .env` is required because the compose file is in a subdirectory.

### Stage 9 — Shared Platform Core
Status: Complete

Modules in `core/`:

| Module | File | Purpose |
|---|---|---|
| config | `core/config/settings.py` | typed settings from `.env` via pydantic-settings |
| logging | `core/logging/logger.py` | structlog structured logger |
| metrics | `core/metrics/metrics.py` | Prometheus counters and histograms |
| database | `core/database/postgres.py` | psycopg3 connection factory |
| redis | `core/redis/redis.py` | redis-py client factory |

Tests:
```bash
PYTHONPATH=. .venv/bin/pytest tests/unit/ -v                        # no containers
PYTHONPATH=. .venv/bin/pytest tests/integration/ -v -m integration  # containers required
```

---

## Onboarding — Reproduce This Phase

### 1. Docker

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
# restart terminal (WSL users: restart WSL)
sudo service docker start
docker run hello-world
```

### 2. Persistent Storage

```bash
sudo mkdir -p /var/lib/data/volumes/cognitive-platform/{postgres,redis,prometheus,grafana}
sudo chmod -R 777 /var/lib/data
```

### 3. Start Infrastructure

```bash
docker compose -f docker/cognitive-compose.yml --env-file .env up -d
docker ps
```

Expected containers: cognitive-postgres, cognitive-redis, cognitive-prometheus,
cognitive-grafana, cognitive-postgres-exporter, cognitive-redis-exporter

### 4. Verify

```bash
# Postgres
docker exec -it cognitive-postgres psql -U cognitive -d cognitive -c "\conninfo"

# pgvector
docker exec -it cognitive-postgres psql -U cognitive -d cognitive \
  -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Redis
docker exec -it cognitive-redis redis-cli ping   # → PONG

# Prometheus: http://localhost:9090
# Grafana:    http://localhost:3000  (admin / admin)
```

### 5. Python Runtime

```bash
source .venv/bin/activate
pip install fastapi uvicorn prometheus-client "psycopg[binary]" redis \
            pydantic pydantic-settings structlog \
            pytest httpx black ruff
```

### 6. Verify Core Modules

```bash
PYTHONPATH=. .venv/bin/python scripts/test_core.py
```

Expected:
```
testing_platform_core
Postgres connected
Redis ping: True
```

---

## Progress Tracking

- [x] Docker installed and running
- [x] Persistent storage directories created
- [x] Postgres + pgvector container running
- [x] Redis container running
- [x] Prometheus container running and scraping
- [x] Grafana running and accessible
- [x] postgres-exporter running
- [x] redis-exporter running
- [x] WSL snapshot backup script working
- [x] Python runtime packages installed
- [x] Docker Compose split into structured layout
- [x] `core/config` implemented and tested
- [x] `core/logging` implemented and tested
- [x] `core/metrics` implemented and tested
- [x] `core/database` implemented and tested
- [x] `core/redis` implemented and tested
- [x] Unit tests passing (no containers)
- [x] Integration tests passing (live containers)

---

## Next Phase

Phase 3 — Mini GPT: transformer model from scratch using PyTorch.
See [phases-overview.md — Phase 3](phases-overview.md#phase-3--mini-gpt)
