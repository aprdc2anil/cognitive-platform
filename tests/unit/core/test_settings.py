from core.config.settings import Settings


def test_default_values():
    s = Settings()
    assert s.APP_NAME == "cognitive-platform"
    assert s.POSTGRES_PORT == 5432
    assert s.REDIS_PORT == 6379
    assert s.PROMETHEUS_ENABLED is True


def test_override_via_env(monkeypatch):
    monkeypatch.setenv("APP_NAME", "test-platform")
    monkeypatch.setenv("POSTGRES_PORT", "5433")
    s = Settings()
    assert s.APP_NAME == "test-platform"
    assert s.POSTGRES_PORT == 5433
