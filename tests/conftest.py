import pytest
import sqlite3
import database


@pytest.fixture
def test_db():
    """her test icin bos in-memory db olustur ve paylas"""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    database.set_shared_connection(conn)
    database.init_db()
    yield ":memory:"
    database.clear_shared_connection()
    conn.close()