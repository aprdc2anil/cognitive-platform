from unittest.mock import patch, MagicMock
from core.redis.redis import get_redis


def test_get_redis_returns_client():
    mock_client = MagicMock()
    with patch("core.redis.redis.redis.Redis", return_value=mock_client) as mock_redis:
        client = get_redis()
        assert client is mock_client
        mock_redis.assert_called_once()


def test_get_redis_uses_settings():
    from core.config.settings import settings
    with patch("core.redis.redis.redis.Redis") as mock_redis:
        get_redis()
        call_kwargs = mock_redis.call_args.kwargs
        assert call_kwargs["host"] == settings.REDIS_HOST
        assert call_kwargs["port"] == settings.REDIS_PORT
        assert call_kwargs["decode_responses"] is True
