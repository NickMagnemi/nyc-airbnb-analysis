"""Turns a file pattern into the DuckDB expression that reads it.

Design note: you might expect a CsvReader, ParquetReader, JsonReader and
ExcelReader class. Look at what they'd contain, though: each one only differs
by the DuckDB function it calls (read_csv, read_parquet, ...) and its default
options. When classes differ only in DATA, not behaviour, one class configured
with that data is cleaner than four near-copies. That is the main lesson here.

SOLID:
- Interface segregation: Reader asks for one method, nothing more.
- Liskov substitution: every Reader returns an expression usable after FROM,
  so the loader never needs to know which format it's reading.
- Open/closed: a new format is one new entry in READERS.

C# equivalent: Reader is an interface; READERS is like a factory registered in
your DI container, mapping a key to an implementation.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Protocol

from duckpipe.errors import ConfigError  # noqa: F401 - for reader_for


class Reader(Protocol):
    """Anything that can describe how DuckDB should read a set of files.

    A Protocol is Python's version of an interface: any class with a matching
    `table_expression` method counts as a Reader, with no inheritance needed.
    """

    def table_expression(self, files: str, options: Mapping[str, object]) -> str:
        """Return SQL like read_csv('data/x_*.csv', all_varchar = true)."""
        ...


@dataclass(frozen=True)
class TableFunctionReader:
    """A Reader that calls one DuckDB table function, such as read_csv."""

    function_name: str
    default_options: Mapping[str, object] = field(default_factory=dict)

    def table_expression(self, files: str, options: Mapping[str, object]) -> str:
        """Return `function_name('files', defaults merged with options)`.

        Options from pipeline.toml win over the defaults.
        """
        # TODO:
        # 1. Merge: {**self.default_options, **options}
        # 2. Quote `files` with string_literal and render the merged options
        #    with render_options (both from duckpipe.sql_safety).
        # 3. Return e.g. "read_csv('data/x.csv', filename = true)", leaving out
        #    the ", ..." part when there are no options.
        raise NotImplementedError


# filename = true adds a column with each row's source file, which the loader
# needs to fill filename_column. union_by_name lines up columns that moved or
# appeared between files. Excel files are read one at a time, so neither applies.
READERS: Mapping[str, Reader] = {
    "csv": TableFunctionReader("read_csv", {"filename": True, "union_by_name": True}),
    "parquet": TableFunctionReader(
        "read_parquet", {"filename": True, "union_by_name": True}
    ),
    "json": TableFunctionReader("read_json", {"filename": True, "union_by_name": True}),
    "excel": TableFunctionReader("read_xlsx"),
}


def reader_for(format_name: str) -> Reader:
    """Return the Reader registered for `format_name`, or raise ConfigError."""
    # TODO: look it up in READERS; for an unknown format, list the supported
    #       ones in the error message so the fix is obvious.
    raise NotImplementedError
