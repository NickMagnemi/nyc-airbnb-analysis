"""Reads pipeline.toml into typed, read-only settings objects.

Everything specific to one dataset lives in pipeline.toml, so the rest of the
code never has to change for new data (the open/closed principle).

C# equivalent: appsettings.json bound to strongly typed options classes, where
these frozen dataclasses play the role of C# records.

TOML is read with tomllib from the standard library, which only parses data
and can't run code, so a config file can never execute anything.
"""

import tomllib  # noqa: F401 - you'll use this in load_config
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

from duckpipe.errors import ConfigError  # noqa: F401 - for your validation

SUPPORTED_FORMATS = frozenset({"csv", "parquet", "json", "excel"})


@dataclass(frozen=True)
class SourceConfig:
    """One kind of input file and the raw table it loads into.

    Example (TOML):
        [[sources]]
        table = "raw_listings"
        path = "listings_*.csv.gz"
        format = "csv"
        filename_column = "snapshot_date"
        filename_pattern = '(\\d{4}-\\d{2}-\\d{2})'
        options = { all_varchar = true }
    """

    table: str
    path: str  # glob pattern, relative to PipelineConfig.data_dir
    format: str  # one of SUPPORTED_FORMATS
    options: Mapping[str, object] = field(default_factory=dict)  # passed to the reader
    filename_column: str | None = None  # new column filled from each file's name
    filename_pattern: str | None = None  # regex with ONE group, run on the file name
    downloads: Mapping[str, str] = field(default_factory=dict)  # file name -> URL


@dataclass(frozen=True)
class CheckConfig:
    """One data quality check on one table.

    Example (TOML):
        [[checks]]
        table = "raw_listings"
        kind = "not_null"
        column = "id"
    Everything except `table` and `kind` goes into `params`.
    """

    table: str
    kind: str
    params: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class OutputConfig:
    """Somewhere to send finished tables. Everything except `kind` goes in `params`."""

    kind: str
    params: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class PipelineConfig:
    """The whole pipeline: where data lives and every stage's settings."""

    database: Path
    data_dir: Path
    allowed_hosts: tuple[str, ...] = ()
    sources: tuple[SourceConfig, ...] = ()
    checks: tuple[CheckConfig, ...] = ()
    transforms: tuple[Path, ...] = ()
    outputs: tuple[OutputConfig, ...] = ()
    output_tables: tuple[str, ...] = ()  # finished tables the outputs receive


def load_config(path: Path) -> PipelineConfig:
    """Read and validate `path`, returning a PipelineConfig.

    Raise ConfigError with a clear message for any missing or invalid setting,
    so mistakes are caught before any data is touched.
    """
    # TODO:
    # 1. Open the file in binary mode ("rb") and parse it with tomllib.load.
    #    Turn tomllib.TOMLDecodeError into ConfigError (use `raise ... from error`).
    # 2. Build each SourceConfig with _parse_source, each CheckConfig with
    #    _parse_check, each OutputConfig with _parse_output.
    # 3. Paths in the file are relative to the file's folder: path.parent / value.
    # 4. Return a PipelineConfig. Use tuples, not lists, so it stays read-only.
    raise NotImplementedError


def _parse_source(raw: Mapping[str, object]) -> SourceConfig:
    """Build a SourceConfig from one [[sources]] table, validating it."""
    # TODO: check required keys exist (table, path, format) and that format is
    #       in SUPPORTED_FORMATS. If only one of filename_column/filename_pattern
    #       is set, that's an error: they only make sense together.
    raise NotImplementedError


def _parse_check(raw: Mapping[str, object]) -> CheckConfig:
    """Build a CheckConfig: pull out `table` and `kind`, the rest becomes params."""
    # TODO: a dict comprehension that skips "table" and "kind" builds params.
    raise NotImplementedError


def _parse_output(raw: Mapping[str, object]) -> OutputConfig:
    """Build an OutputConfig: pull out `kind`, the rest becomes params."""
    # TODO
    raise NotImplementedError
