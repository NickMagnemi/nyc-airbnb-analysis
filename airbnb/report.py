"""Summaries to check that a load worked."""

import duckdb

from airbnb.safe_sql import is_safe_identifier


def count_rows_by_snapshot(
    con: duckdb.DuckDBPyConnection, table: str
) -> duckdb.DuckDBPyRelation:
    """Return the number of rows in each snapshot of `table`, oldest first."""
    query = f"""
        SELECT snapshot_date, COUNT(*) AS row_count
        FROM {is_safe_identifier(table)}
        GROUP BY snapshot_date
        ORDER BY snapshot_date
    """  # Table name validated by safe_identifier
    return con.sql(query)