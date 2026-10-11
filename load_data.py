"""Load every configured source into the project database."""

import duckdb

from airbnb.config import DATA_DIR, DATABASE_PATH, SOURCES
from airbnb.load import load_snapshots
from airbnb.report import count_rows_by_snapshot


def main() -> None:
    with duckdb.connect(str(DATABASE_PATH)) as con:
        for table, pattern in SOURCES.items():
            load_snapshots(con, table, DATA_DIR / pattern)
            print(table)
            count_rows_by_snapshot(con, table).show()


if __name__ == "__main__":
    main()