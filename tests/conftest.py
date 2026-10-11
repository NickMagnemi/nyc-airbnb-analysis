"""Shared test fixtures. pytest loads this file automatically."""

import duckdb
import pytest


@pytest.fixture
def connection():
    """A fresh in-memory database for each test, closed afterwards."""
    con = duckdb.connect()
    yield con
    con.close()
