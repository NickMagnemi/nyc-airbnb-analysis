"""Data quality checks that run on a table before anyone trusts it.

Each kind of check is its own small class with a single `run` method, so:
- Single responsibility: one class, one rule.
- Open/closed: a new rule is a new class plus one line in CHECK_TYPES.
- Liskov substitution: every check returns a CheckResult; none of them raise
  for bad data, so CheckRunner can treat them all the same way.

Column names come from the data, so always pass them through quote_identifier.
Table names come from your config, so they go through validate_table_name.
Numbers (like a minimum row count) are query parameters (?), never formatted in.

C# equivalent: like FluentValidation, where each rule is a small class and a
validator runs them all and collects the failures.
"""

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Protocol

from duckpipe.config import CheckConfig
from duckpipe.connection import Connection


@dataclass(frozen=True)
class CheckResult:
    """The outcome of one check on one table."""

    check: str  # e.g. "not_null(id)"
    table: str
    passed: bool
    message: str  # what went wrong, or "ok"


class Check(Protocol):
    """Anything that can test one rule against a table."""

    @property
    def name(self) -> str:
        """Short description for reports, e.g. "unique(id, snapshot_date)"."""
        ...

    def run(self, connection: Connection, table: str) -> CheckResult:
        """Test the rule and return the result. Never raise for bad data."""
        ...


def _count(
    connection: Connection, query: str, parameters: Sequence[object] = ()
) -> int:
    """Run a COUNT(*) query and return the number, or 0 if nothing came back.

    You wrote this in the first project; port it over and add `parameters`.
    """
    # TODO
    raise NotImplementedError


@dataclass(frozen=True)
class RequiredColumns:
    """Every listed column must exist in the table."""

    columns: tuple[str, ...]

    @property
    def name(self) -> str:
        return f"required_columns({', '.join(self.columns)})"

    def run(self, connection: Connection, table: str) -> CheckResult:
        # TODO: get the table's columns with DESCRIBE (as in the first project),
        #       work out which required ones are missing with a set difference,
        #       and return a failing CheckResult that lists them, sorted.
        raise NotImplementedError


@dataclass(frozen=True)
class NotNull:
    """A column must have no NULL values."""

    column: str

    @property
    def name(self) -> str:
        return f"not_null({self.column})"

    def run(self, connection: Connection, table: str) -> CheckResult:
        # TODO: count rows WHERE <quoted column> IS NULL with _count.
        raise NotImplementedError


@dataclass(frozen=True)
class Unique:
    """No two rows may share the same values in these columns."""

    columns: tuple[str, ...]

    @property
    def name(self) -> str:
        return f"unique({', '.join(self.columns)})"

    def run(self, connection: Connection, table: str) -> CheckResult:
        # TODO: count groups with GROUP BY <quoted columns> HAVING COUNT(*) > 1,
        #       wrapped in SELECT COUNT(*) FROM (...), like your duplicate-id check.
        raise NotImplementedError


@dataclass(frozen=True)
class MinRows:
    """The table, or each group when `per` is set, must have at least `minimum` rows."""

    minimum: int
    per: str | None = None  # e.g. "snapshot_date" checks each snapshot separately

    @property
    def name(self) -> str:
        return f"min_rows({self.minimum}{f' per {self.per}' if self.per else ''})"

    def run(self, connection: Connection, table: str) -> CheckResult:
        # TODO: without `per`, compare COUNT(*) to minimum. With `per`, find the
        #       groups that fall short (GROUP BY ... HAVING COUNT(*) < ?) and name
        #       them in the message. Pass minimum as a parameter.
        raise NotImplementedError


# kind in pipeline.toml -> function that builds the check from its params.
# Lambdas turn TOML lists into tuples, so every check stays immutable.
# Any is used because TOML values can be any type; build_check validates them.
CHECK_TYPES: Mapping[str, Callable[[Mapping[str, Any]], Check]] = {
    "required_columns": lambda p: RequiredColumns(tuple(p["columns"])),
    "not_null": lambda p: NotNull(p["column"]),
    "unique": lambda p: Unique(tuple(p["columns"])),
    "min_rows": lambda p: MinRows(int(p["minimum"]), p.get("per")),
}


def build_check(config: CheckConfig) -> Check:
    """Create the Check described by `config`; raise ConfigError if unknown."""
    # TODO: look up config.kind in CHECK_TYPES. A KeyError from a missing param
    #       should also become a ConfigError naming the check and the param.
    raise NotImplementedError


class CheckRunner:
    """Runs a set of checks and decides whether the pipeline may continue."""

    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def run_all(self, checks: Sequence[tuple[str, Check]]) -> list[CheckResult]:
        """Run every (table, check) pair and return all results, passed or not.

        Running them all, instead of stopping at the first failure, means one
        run shows you every problem at once.
        """
        # TODO: a list comprehension calling check.run(self._connection, table).
        raise NotImplementedError

    @staticmethod
    def raise_if_failed(results: Sequence[CheckResult]) -> None:
        """Raise CheckFailedError listing every failed result, if there are any."""
        # TODO: filter to failures; build one message line per failure.
        raise NotImplementedError
