import pytest
from core.database.postgres import get_connection


@pytest.mark.integration
def test_postgres_connection():
    conn = get_connection()
    assert conn is not None
    conn.close()


@pytest.mark.integration
def test_postgres_query():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT 1")
        result = cur.fetchone()
    conn.close()
    assert result[0] == 1


@pytest.mark.integration
def test_postgres_database_name():
    from core.config.settings import settings
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT current_database()")
        result = cur.fetchone()
    conn.close()
    assert result[0] == settings.POSTGRES_DB
