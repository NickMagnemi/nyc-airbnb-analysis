"""Load raw data Inside Airbnb snapshot files into DuckDB."""

from pathlib import Path

import duckdb

from airbnb.safe_sql import is_safe_identifier, string_literal

SNAPSHOT_DATE_REGEX = r"^\d{4}-\d{2}-\d{2}$"  # Regex to match dates in the format YYYY-MM-DD

def load_snapshots(con: duckdb.DuckDBPyConnection, table: str, files: Path) -> None:
    """Create `table` from every file matching `files`, adding a snapshot_date column.

    Everything is loaded as text so column changes between snapshots never break
    the load. Proper types are set later, in the cleaning step.
    """

    query = f"""
        CREATE OR REPLACE TABLE {is_safe_identifier(table)} AS
        SELECT *,
               CAST(regexp_extract(filename, {string_literal(SNAPSHOT_DATE_REGEX)}, 1)
                    AS DATE) AS snapshot_date
        FROM read_csv({string_literal(str(files))},
                      filename = true,
                      union_by_name = true,
                      all_varchar = true)
    """  # Table name validated and text escaped by safe_sql
    con.execute(query)