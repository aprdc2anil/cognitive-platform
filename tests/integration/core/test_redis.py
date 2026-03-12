import pytest
from core.redis.redis import get_redis


@pytest.mark.integration
def test_redis_ping():
    r = get_redis()
    assert r.ping() is True


@pytest.mark.integration
def test_redis_set_get():
    r = get_redis()
    r.set("test:key", "test-value")
    value = r.get("test:key")
    r.delete("test:key")
    assert value == "test-value"


@pytest.mark.integration
def test_redis_delete():
    r = get_redis()
    r.set("test:delete", "1")
    r.delete("test:delete")
    assert r.get("test:delete") is None
