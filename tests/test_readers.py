import pytest

from duckpipe.errors import ConfigError
from duckpipe.readers import reader_for


def test_csv_reader_uses_its_default_options():
    expression = reader_for("csv").table_expression("data/x_*.csv", {})

    assert expression == (
        "read_csv('data/x_*.csv', filename = true, union_by_name = true)"
    )


def test_options_from_config_override_defaults():
    expression = reader_for("csv").table_expression(
        "data/x.csv", {"filename": False, "all_varchar": True}
    )

    assert expression == (
        "read_csv('data/x.csv', filename = false, union_by_name = true, "
        "all_varchar = true)"
    )


def test_reader_without_options_has_no_trailing_comma():
    assert reader_for("excel").table_expression("data/x.xlsx", {}) == (
        "read_xlsx('data/x.xlsx')"
    )


def test_reader_for_unknown_format_raises_config_error():
    with pytest.raises(ConfigError):
        reader_for("pdf")
