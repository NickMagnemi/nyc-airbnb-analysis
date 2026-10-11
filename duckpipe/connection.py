"""The single place that knows which database library duckpipe uses.

Every other module imports `Connection` from here and receives a connection as
an argument; none of them call duckdb.connect themselves. That is dependency
inversion: tests pass an in-memory database, real runs pass the project file.

C# equivalent: a DbContext you inject through the constructor instead of
`new`-ing it inside each class.
"""

from pathlib import Path

import duckdb

type Connection = duckdb.DuckDBPyConnection


def open_database(path: Path | None = None, *, read_only: bool = False) -> Connection:
    """Open the DuckDB database at `path`, or an in-memory one when `path` is None.

    The `*` makes read_only keyword-only, so callers must write read_only=True,
    which reads more clearly than a bare True.
    """
    # TODO: call duckdb.connect. For in-memory, pass ":memory:".
    #       read_only only makes sense for a file, so ignore it for in-memory.
    raise NotImplementedError
