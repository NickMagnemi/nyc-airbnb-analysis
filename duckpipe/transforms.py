"""Runs your SQL transform files, in order: the "T" in ELT.

Transforms are where dataset-specific knowledge lives: fixing types, cleaning
values, dropping personal fields, building the tables you analyse. They're
plain .sql files in the project, so they're reviewed in pull requests like code.

Security note: transform files are trusted code from your own repo, so they're
executed as written. Never point `transforms` at SQL from outside the project.

C# equivalent: roughly EF Core migrations, but for data rather than schema:
ordered scripts that each build on the last.
"""

from pathlib import Path
from typing import Protocol

from duckpipe.connection import Connection


class Transform(Protocol):
    """Anything that changes data inside the database."""

    @property
    def name(self) -> str: ...

    def apply(self, connection: Connection) -> None: ...


class SqlFileTransform:
    """A Transform defined by one .sql file."""

    def __init__(self, path: Path) -> None:
        self._path = path

    @property
    def name(self) -> str:
        """The file name, for progress messages."""
        return self._path.name

    def apply(self, connection: Connection) -> None:
        """Read the file and execute its SQL.

        A file may hold several statements separated by semicolons; DuckDB's
        execute runs them all.
        """
        # TODO: read the file as UTF-8 text and execute it.
        #       Raise ConfigError (with the path) if the file doesn't exist,
        #       rather than letting a raw FileNotFoundError escape.
        raise NotImplementedError
