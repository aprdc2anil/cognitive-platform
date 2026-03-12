# Cognitive Platform — Phase 2 Developer Onboarding Runbook

## Purpose

Phase 2 establishes the **platform engineering foundation** for the Cognitive Platform.

By the end of Phase 2 the development environment should support:

* Containerized infrastructure
* Persistent data storage
* Observability (metrics + dashboards)
* Logging
* Automated environment backups
* Python service runtime stack

This phase prepares the environment so that all future services (RAG, agents, ML services, copilot) run consistently.

---

# Phase 2 Goals

1. Establish platform infrastructure
2. Standardize storage layout
3. Enable monitoring and logging
4. Implement environment backup strategy
5. Install base runtime stack for services
6. Prepare shared platform core modules

---

# Phase 2 Architecture Overview

```
WSL Linux

  Docker Compose

    ├── Postgres + pgvector
    ├── Redis
    ├── Prometheus
    └── Grafana

  Exporters

    ├── postgres_exporter
    └── redis_exporter

  Python Runtime (.venv)

    ├── FastAPI
    ├── Postgres client
    ├── Redis client
    ├── Prometheus metrics
    └── Structured logging

  Storage

    /var/lib/data/volumes/cognitive-platform

  Backups

    WSL snapshot → Google Drive
```

---

# Phase 2 Stages

## Stage 1 — Platform Repository Structure

Status: Complete

Repository layout:

```
cognitive-platform/

core/
services/
infra/
models/
datasets/
docker/
scripts/
docs/
```

Services placeholders:

```
services/
  rag-service
  agent-service
  ml-service
  copilot-service
```

Infrastructure modules:

```
infra/
  llm-gateway
  event-runtime
```

---

## Stage 2 — Docker Infrastructure Stack

Containers deployed via `docker-compose`:

* Postgres (pgvector)
* Redis
* Prometheus
* Grafana

Docker network:

```
cognitive-network
```

---

## Stage 3 — Persistent Storage Layout

Standardized runtime storage:

```
/var/lib/data/volumes/cognitive-platform/

  postgres
  redis
  prometheus
  grafana
```

These directories persist container state.

---

## Stage 4 — Observability Stack

Monitoring pipeline:

```
Service → Exporter → Prometheus → Grafana
```

Exporters:

* postgres_exporter
* redis_exporter

Prometheus scrapes metrics every 15 seconds.

---

## Stage 5 — Logging Infrastructure

Docker container logging configured using:

```
json-file log driver
max-size: 10m
max-file: 3
```

Logs can be inspected using:

```
docker logs <container>

docker compose -f docker/cognitive-compose.yml --env-file .env logs
```

Applications will log to stdout so Docker captures logs automatically.

---

## Stage 6 — Backup and Recovery

WSL snapshot backups implemented using PowerShell script.

Script location:

```
C:\GDrive\dev\scripts\wslsnapshotscript.ps1
```

Backup destination:

```
C:\GDrive\dev\wsl-backups\ubuntu
```

Features:

* WSL filesystem snapshot
* Retain last 2 backups
* Optional Docker cleanup
* Optional container restart

Snapshots include:

* Docker images
* Container volumes
* Source code
* Python environments

---

## Stage 7 — Service Runtime Stack

Installed in project Python virtual environment.

Activate environment:

```
source .venv/bin/activate
```

Core runtime packages:

```
fastapi
uvicorn
prometheus-client
psycopg[binary]
redis
pydantic
pydantic-settings
structlog
```

Development tooling:

```
black
ruff
pytest
httpx
```

These provide the base runtime for platform services.

---

# Stage 8 --- Split docker compose file

docker/

  infra/
      postgres.yml
      redis.yml

  observability/
      prometheus.yml
      grafana.yml
      exporters.yml

  compose.platform.yml

## Stage 9 — Shared Platform Core

(Not started)

The shared runtime layer will live in:

```
core/
```

Planned modules:

```
core/config
core/logging
core/metrics
core/database
core/redis
```

Every service will depend on these modules.

---

# Phase 2 --- Developer Setup Guide

This section provides step-by-step instructions for developers to
reproduce the Phase 2 platform environment.

The instructions assume:

-   WSL Ubuntu is installed
-   Docker Desktop is configured for WSL
-   Phase 1 environment setup is complete

------------------------------------------------------------------------

# Stage 1 --- Clone and Prepare Repository

Clone the platform repository.

``` bash
cd ~/dev
git clone <your-repo-url> cognitive-platform
cd cognitive-platform
```

Verify repository structure:

``` bash
tree -L 2
```

Expected layout:

    cognitive-platform/

    core/
    services/
    infra/
    models/
    datasets/
    docker/
    scripts/
    docs/

Create service placeholders if not present:

``` bash
mkdir -p services/rag-service
mkdir -p services/agent-service
mkdir -p services/ml-service
mkdir -p services/copilot-service
```

Create infrastructure modules:

``` bash
mkdir -p infra/llm-gateway
mkdir -p infra/event-runtime
```

------------------------------------------------------------------------

# Stage 2 --- Create Docker Infrastructure Stack

Navigate to the docker directory.

``` bash
cd docker
```

Create the Docker Compose file.

``` bash
code docker-compose.yml
```

Example configuration:

``` yaml
version: "3.9"

networks:
  cognitive-network:

services:

  postgres:
    image: ankane/pgvector
    container_name: cognitive-postgres
    restart: unless-stopped
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: cognitive
      POSTGRES_PASSWORD: cognitive
      POSTGRES_DB: cognitive
    volumes:
      - /var/lib/data/volumes/cognitive-platform/postgres:/var/lib/postgresql/data
    networks:
      - cognitive-network

  redis:
    image: redis:7
    container_name: cognitive-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - /var/lib/data/volumes/cognitive-platform/redis:/data
    networks:
      - cognitive-network

  prometheus:
    image: prom/prometheus
    container_name: cognitive-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - /var/lib/data/volumes/cognitive-platform/prometheus:/prometheus
    networks:
      - cognitive-network

  grafana:
    image: grafana/grafana
    container_name: cognitive-grafana
    ports:
      - "3000:3000"
    volumes:
      - /var/lib/data/volumes/cognitive-platform/grafana:/var/lib/grafana
    networks:
      - cognitive-network
```

------------------------------------------------------------------------

# Stage 3 --- Create Persistent Storage Directories

Create the persistent data directories.

``` bash
sudo mkdir -p /var/lib/data/volumes/cognitive-platform
```

Create service directories:

``` bash
sudo mkdir -p /var/lib/data/volumes/cognitive-platform/postgres
sudo mkdir -p /var/lib/data/volumes/cognitive-platform/redis
sudo mkdir -p /var/lib/data/volumes/cognitive-platform/prometheus
sudo mkdir -p /var/lib/data/volumes/cognitive-platform/grafana
```

Set permissions:

``` bash
sudo chmod -R 777 /var/lib/data
```

Verify:

``` bash
tree /var/lib/data
```

------------------------------------------------------------------------

# Stage 4 --- Configure Prometheus Monitoring

Create configuration file:

``` bash
cd docker
code prometheus.yml
```

Example configuration:

``` yaml
global:
  scrape_interval: 15s

scrape_configs:

  - job_name: "postgres"
    static_configs:
      - targets: ["postgres_exporter:9187"]

  - job_name: "redis"
    static_configs:
      - targets: ["redis_exporter:9121"]
```

------------------------------------------------------------------------

# Stage 5 --- Configure Docker Logging

Add logging configuration to containers in `docker-compose.yml`.

Example:

``` yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

View logs:

``` bash
docker compose -f docker/cognitive-compose.yml --env-file .env logs
```

Or container specific logs:

``` bash
docker logs cognitive-postgres
```

------------------------------------------------------------------------

# Stage 6 --- Setup Backup Script

Create PowerShell backup script.

Location:

    C:\GDrive\dev\scripts\wslsnapshotscript.ps1

Example script structure:

``` powershell
$backupDir = "C:\GDrive\dev\wsl-backups\ubuntu"
$timestamp = Get-Date -Format "yyyyMMddHHmm"

wsl --export Ubuntu "$backupDir\ubuntu-$timestamp.tar"

Get-ChildItem $backupDir |
Sort CreationTime -Descending |
Select -Skip 2 |
Remove-Item
```

Run backup manually:

``` powershell
powershell -ExecutionPolicy Bypass -File C:\GDrive\dev\scripts\wslsnapshotscript.ps1
```

script sample available in - cognitive-platform/scripts

Verify backup exists:

    C:\GDrive\dev\wsl-backups\ubuntu

------------------------------------------------------------------------

# Stage 7 --- Setup Python Runtime Environment

Navigate to project root.

``` bash
cd ~/dev/cognitive-platform
```

Create Python virtual environment.

``` bash
python3 -m venv .venv
```

Activate environment.

``` bash
source .venv/bin/activate
```

Upgrade pip.

``` bash
pip install --upgrade pip
```

Install runtime packages.

``` bash
pip install fastapi uvicorn prometheus-client psycopg[binary] redis pydantic pydantic-settings structlog
```

Install development tools.

``` bash
pip install black ruff pytest httpx
```

Verify installation.

``` bash
pip list
```

------------------------------------------------------------------------

# Stage8 : Docker compose split

# Stage 9 : Core setup with basic tests

Implements shared platform core modules used by all services.

------------------------------------------------------------------------

## Step 1 — Directory Structure

Directories are pre-created under `core/`:

    core/
    ├── __init__.py
    ├── config/
    │   ├── __init__.py
    │   └── settings.py
    ├── logging/
    │   ├── __init__.py
    │   └── logger.py
    ├── metrics/
    │   ├── __init__.py
    │   └── metrics.py
    ├── database/
    │   ├── __init__.py
    │   └── postgres.py
    └── redis/
        ├── __init__.py
        └── redis.py

------------------------------------------------------------------------

## Step 2 — Configuration Module

`core/config/settings.py` uses `pydantic-settings` to load config from environment / `.env`.

Extra keys in `.env` (e.g. `HOST_VOLUMES_PATH`, `ANTHROPIC_API_KEY`) are ignored via `extra="ignore"`.

``` python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "cognitive-platform"

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "cognitive"
    POSTGRES_USER: str = "cognitive"
    POSTGRES_PASSWORD: str = "cognitive"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    PROMETHEUS_ENABLED: bool = True


settings = Settings()
```

------------------------------------------------------------------------

## Step 3 — Logging Module

`core/logging/logger.py` uses `structlog` for structured JSON-friendly logging.

``` python
import structlog
import logging

logging.basicConfig(format="%(message)s", level=logging.INFO)

logger = structlog.get_logger()
```

Usage in services:

``` python
from core.logging.logger import logger

logger.info("service_started", service="rag-service")
```

------------------------------------------------------------------------

## Step 4 — Prometheus Metrics

`core/metrics/metrics.py` defines base counters and histograms with labels.

``` python
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "Request latency",
    ["method", "endpoint"],
)
```

Services expose metrics via FastAPI middleware in later phases.

------------------------------------------------------------------------

## Step 5 — Postgres Client

`core/database/postgres.py` provides a connection factory using psycopg3.

``` python
import psycopg
from core.config.settings import settings


def get_connection() -> psycopg.Connection:
    return psycopg.connect(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        dbname=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
    )
```

------------------------------------------------------------------------

## Step 6 — Redis Client

`core/redis/redis.py` provides a Redis client factory.

``` python
import redis
from core.config.settings import settings


def get_redis() -> redis.Redis:
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True,
    )
```

------------------------------------------------------------------------

## Step 7 — Tests

Tests are split into unit and integration suites:

    tests/
    ├── unit/core/          # mocked, no containers required
    │   ├── test_settings.py
    │   ├── test_logger.py
    │   ├── test_metrics.py
    │   ├── test_postgres.py
    │   └── test_redis.py
    └── integration/core/   # hits live containers
        ├── test_postgres.py
        └── test_redis.py

Integration tests are marked with `@pytest.mark.integration` and defined in `pytest.ini`.

Run unit tests only:

``` bash
PYTHONPATH=. .venv/bin/pytest tests/unit/ -v
```

Run integration tests (containers must be up):

``` bash
PYTHONPATH=. .venv/bin/pytest tests/integration/ -v -m integration
```

Run all tests:

``` bash
PYTHONPATH=. .venv/bin/pytest -v
```

Run all except integration:

``` bash
PYTHONPATH=. .venv/bin/pytest -v -m "not integration"
```

------------------------------------------------------------------------

## Step 8 — Quick Platform Smoke Test

``` bash
PYTHONPATH=. .venv/bin/python scripts/test_core.py
```

Expected output:

    testing_platform_core
    Postgres connected
    Redis ping: True

------------------------------------------------------------------------

# Expected Outcome

After completing Stage 9:

-   Docker infrastructure runs successfully
-   Persistent storage directories exist
-   Prometheus collects metrics
-   Grafana dashboards accessible
-   Python runtime environment ready
-   Shared `core/` modules implemented and tested
-   Unit tests pass without running containers
-   Integration tests pass against live containers





# Phase 2 Completion Criteria

Phase 2 is complete when:

* Infrastructure containers run successfully
* Persistent storage directories exist
* Metrics visible in Grafana
* Logs accessible via Docker
* WSL snapshot backups working
* Python runtime stack installed
* Shared platform core modules ready to implement

---

# Next Phase

Phase 3 introduces model development via the MiniGPT implementation.

Before entering Phase 3, the shared platform runtime (`core/`) should be implemented.
