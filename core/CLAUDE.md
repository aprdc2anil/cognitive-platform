# core/ — CLAUDE.md

## Purpose

Shared platform modules used by every service and model in this repo.
Never reimplement config, logging, metrics, db, or redis inside a service — import from here.

---

## Modules

### config — `core/config/settings.py`

Typed settings loaded from `.env` via pydantic-settings. Extra keys in `.env` are ignored.

```python
from core.config.settings import settings

settings.POSTGRES_HOST
settings.POSTGRES_PORT
settings.POSTGRES_DB
settings.POSTGRES_USER
settings.POSTGRES_PASSWORD
settings.REDIS_HOST
settings.REDIS_PORT
settings.PROMETHEUS_ENABLED
settings.APP_NAME
```

Override via environment variables or `.env`. All fields have safe defaults so unit tests work without `.env`.

---

### logging — `core/logging/logger.py`

Structured logging via structlog. Always use key=value style — this makes logs parseable.

```python
from core.logging.logger import logger

logger.info("service_started", service="rag-service")
logger.error("connection_failed", host=settings.POSTGRES_HOST, error=str(e))
```

---

### metrics — `core/metrics/metrics.py`

Prometheus counters and histograms. Services expose these via FastAPI middleware in later phases.

```python
from core.metrics.metrics import REQUEST_COUNT, REQUEST_LATENCY

REQUEST_COUNT.labels(method="GET", endpoint="/health", status="200").inc()

with REQUEST_LATENCY.labels(method="GET", endpoint="/health").time():
    ...
```

---

### database — `core/database/postgres.py`

psycopg3 connection factory. Returns a raw connection — caller manages lifecycle.

```python
from core.database.postgres import get_connection

conn = get_connection()
with conn.cursor() as cur:
    cur.execute("SELECT 1")
conn.close()
```

For services, wrap in a context manager or dependency injection. pgvector extension is enabled on the running container.

---

### redis — `core/redis/redis.py`

redis-py client factory. Returns a connected client with `decode_responses=True`.

```python
from core.redis.redis import get_redis

r = get_redis()
r.set("key", "value", ex=60)
val = r.get("key")
r.ping()
```

---

## Tests

```
tests/unit/core/       # mocked — no containers
tests/integration/core/  # live — containers must be running
```

Run unit only:
```bash
PYTHONPATH=. .venv/bin/pytest tests/unit/core/ -v
```

Run integration only:
```bash
PYTHONPATH=. .venv/bin/pytest tests/integration/core/ -v -m integration
```

Integration tests verify real connectivity to `cognitive-postgres` and `cognitive-redis`.

---

## Adding a New Core Module

1. Create `core/<module>/` directory
2. Add `core/<module>/__init__.py`
3. Implement in `core/<module>/<module>.py`
4. Add unit tests in `tests/unit/core/test_<module>.py`
5. Add integration tests in `tests/integration/core/test_<module>.py` if it touches infra
6. Export from `core/__init__.py` if needed for convenience
