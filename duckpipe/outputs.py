"""Sends finished tables somewhere outside the DuckDB file.

Every Output has one method, `write`, so the pipeline can export to any mix of
destinations without knowing what they are (dependency inversion + open/closed).

Security: database credentials are NEVER in pipeline.toml. The config names the
environment variables to read (from .env), and the values stay out of Git.
"""

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, Self

from duckpipe.config import OutputConfig
from duckpipe.connection import Connection


class Output(Protocol):
    """Anything that can receive a set of tables."""

    def write(self, connection: Connection, tables: Sequence[str]) -> None: ...


@dataclass(frozen=True)
class ParquetExport:
    """Writes each table to <directory>/<table>.parquet.

    Parquet is a compressed, typed file format that most data tools can read,
    which makes it a good hand-off format.
    """

    directory: Path

    def write(self, connection: Connection, tables: Sequence[str]) -> None:
        # TODO: create the directory; for each table, run
        #       COPY <validated table> TO '<path>' (FORMAT parquet)
        #       using validate_table_name and string_literal.
        raise NotImplementedError


@dataclass(frozen=True)
class PostgresSettings:
    """Connection settings for PostgreSQL, read from environment variables."""

    host: str
    port: str
    dbname: str
    user: str
    password: str

    @classmethod
    def from_env(cls, prefix: str = "POSTGRES_") -> Self:
        """Read <prefix>HOST, <prefix>PORT, ... from the environment.

        Raise ConfigError naming any missing variable, but never print a value.
        """
        # TODO: import os at the top of the file. Use os.environ.get for host
        #       (default "127.0.0.1") and port (default "5432"); the rest are required.
        raise NotImplementedError

    def dsn(self) -> str:
        """Return a libpq connection string. Contains the password: never log it."""
        # TODO: "host=... port=... dbname=... user=... password=..."
        raise NotImplementedError

    def __repr__(self) -> str:
        """Hide the password if this object is ever printed or logged."""
        return (
            f"PostgresSettings(host={self.host!r}, dbname={self.dbname!r}, "
            f"user={self.user!r}, password='***')"
        )


@dataclass(frozen=True)
class PostgresExport:
    """Copies tables into PostgreSQL through DuckDB's postgres extension."""

    settings: PostgresSettings

    def write(self, connection: Connection, tables: Sequence[str]) -> None:
        # TODO:
        # 1. INSTALL postgres; LOAD postgres;
        # 2. ATTACH <string_literal(dsn)> AS pg (TYPE postgres)
        # 3. For each table: CREATE OR REPLACE TABLE pg.<table> AS SELECT * FROM <table>
        # 4. DETACH pg in a `finally` block, so it always disconnects.
        raise NotImplementedError


# kind in pipeline.toml -> function that builds the Output from its params.
OUTPUT_TYPES: Mapping[str, Callable[[Mapping[str, Any]], Output]] = {
    "parquet": lambda p: ParquetExport(Path(p["directory"])),
    "postgres": lambda p: PostgresExport(
        PostgresSettings.from_env(p.get("env_prefix", "POSTGRES_"))
    ),
}


def build_output(config: OutputConfig) -> Output:
    """Create the Output described by `config`, or raise ConfigError."""
    # TODO: same pattern as build_check in checks.py.
    raise NotImplementedError

