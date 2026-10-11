"""Loads raw files into tables, unchanged apart from one optional extra column.

This is the "L" in ELT: data lands as-is, and cleaning happens later in SQL
transforms, so you always keep an untouched copy of the source.

Single responsibility: TableLoader knows how to CREATE a table from a source.
It doesn't know file formats (that's the Reader) or what "good data" means
(that's the checks).
"""

from pathlib import Path

from duckpipe.config import SourceConfig
from duckpipe.connection import Connection
from duckpipe.readers import Reader


class TableLoader:
    """Creates or replaces one raw table per source."""

    def __init__(self, connection: Connection, data_dir: Path) -> None:
        """Store the collaborators. C#: constructor injection."""
        self._connection = connection
        self._data_dir = data_dir

    def load(self, source: SourceConfig, reader: Reader) -> None:
        """Create `source.table` from every file matching `source.path`.

        The SQL you're building looks like:
            CREATE OR REPLACE TABLE raw_listings AS
            SELECT *, <extra column, if configured>
            FROM read_csv('data/listings_*.csv.gz', ...)
        """
        # TODO:
        # 1. Validate the table name with validate_table_name.
        # 2. Build the FROM part: reader.table_expression(str(self._data_dir /
        #    source.path), source.options).
        # 3. Add self._filename_column_sql(source) to the SELECT list when it's
        #    not empty.
        # 4. Execute it. Add `# noqa: S608` with a reason, as in the first project.
        raise NotImplementedError

    def _filename_column_sql(self, source: SourceConfig) -> str:
        """Return the SQL for the extra column, or "" if none is configured.

        Example result:
            regexp_extract(filename, '(\\d{4}-\\d{2}-\\d{2})', 1) AS "snapshot_date"
        """
        # TODO: return "" when source.filename_column is None. Otherwise use
        #       string_literal for the pattern and quote_identifier for the
        #       column name. Converting the text to a DATE belongs in a
        #       transform, not here: the loader doesn't guess types.
        raise NotImplementedError
