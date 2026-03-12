import pytest
from unittest.mock import patch, MagicMock
from core.database.postgres import get_connection


def test_get_connection_calls_psycopg_connect():
    mock_conn = MagicMock()
    with patch("core.database.postgres.psycopg.connect", return_value=mock_conn) as mock_connect:
        conn = get_connection()
        assert conn is mock_conn
        mock_connect.assert_called_once()


def test_get_connection_uses_settings():
    from core.config.settings import settings
    with patch("core.database.postgres.psycopg.connect") as mock_connect:
        get_connection()
        call_kwargs = mock_connect.call_args.kwargs
        assert call_kwargs["host"] == settings.POSTGRES_HOST
        assert call_kwargs["port"] == settings.POSTGRES_PORT
        assert call_kwargs["dbname"] == settings.POSTGRES_DB
        assert call_kwargs["user"] == settings.POSTGRES_USER
        assert call_kwargs["password"] == settings.POSTGRES_PASSWORD
