import pytest

from duckpipe.checks import (
    CheckResult,
    CheckRunner,
    MinRows,
    NotNull,
    RequiredColumns,
    Unique,
    build_check,
)
from duckpipe.config import CheckConfig
from duckpipe.errors import CheckFailedError, ConfigError


@pytest.fixture
def items(connection):
    """A small table with known problems. "Item Name" has a space on purpose."""
    connection.execute(
        """
        CREATE TABLE items AS
        SELECT * FROM (VALUES
            (1, 'apple', '2025-01-15'),
            (1, 'pear', '2025-01-15'),
            (NULL, 'plum', '2025-01-15')
        ) AS t(id, "Item Name", snapshot_date)
        """
    )
    return connection


def test_required_columns_passes_when_all_exist(items):
    assert RequiredColumns(("id", "Item Name")).run(items, "items").passed


def test_required_columns_names_the_missing_ones(items):
    result = RequiredColumns(("id", "price")).run(items, "items")

    assert not result.passed
    assert "price" in result.message


def test_not_null_fails_and_counts_nulls(items):
    result = NotNull("id").run(items, "items")

    assert not result.passed
    assert "1" in result.message


def test_not_null_handles_column_names_with_spaces(items):
    assert NotNull("Item Name").run(items, "items").passed


def test_unique_fails_on_duplicates(items):
    assert not Unique(("id", "snapshot_date")).run(items, "items").passed


def test_unique_passes_when_values_differ(items):
    assert Unique(("Item Name",)).run(items, "items").passed


@pytest.mark.parametrize(("minimum", "passed"), [(3, True), (4, False)])
def test_min_rows_for_whole_table(items, minimum, passed):
    assert MinRows(minimum).run(items, "items").passed is passed


def test_min_rows_per_group_names_the_short_group(items):
    result = MinRows(4, per="snapshot_date").run(items, "items")

    assert not result.passed
    assert "2025-01-15" in result.message


def test_build_check_creates_the_configured_check():
    config = CheckConfig(table="items", kind="not_null", params={"column": "id"})

    assert build_check(config) == NotNull("id")


@pytest.mark.parametrize(
    "config",
    [
        CheckConfig(table="items", kind="no_such_check"),
        CheckConfig(table="items", kind="not_null", params={}),
    ],
)
def test_build_check_rejects_bad_config(config):
    with pytest.raises(ConfigError):
        build_check(config)


def test_raise_if_failed_raises_only_when_something_failed():
    passed = CheckResult("not_null(id)", "items", True, "ok")
    failed = CheckResult("unique(id)", "items", False, "1 duplicate group")

    CheckRunner.raise_if_failed([passed])
    with pytest.raises(CheckFailedError):
        CheckRunner.raise_if_failed([passed, failed])
