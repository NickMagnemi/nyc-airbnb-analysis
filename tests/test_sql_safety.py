import pytest

from duckpipe.errors import UnsafeSqlError
from duckpipe.sql_safety import (
    quote_identifier,
    render_options,
    string_literal,
    validate_table_name,
)


def test_validate_table_name_accepts_plain_names():
    assert validate_table_name("raw_listings") == "raw_listings"


@pytest.mark.parametrize(
    "name", ["", "Listings", "raw listings", "x; DROP TABLE y", "1table"]
)
def test_validate_table_name_rejects_unsafe_names(name):
    with pytest.raises(UnsafeSqlError):
        validate_table_name(name)


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("price", '"price"'),
        ("Neighbourhood Group", '"Neighbourhood Group"'),
        ('a"b', '"a""b"'),
    ],
)
def test_quote_identifier_wraps_and_escapes(name, expected):
    assert quote_identifier(name) == expected


def test_quote_identifier_rejects_empty_name():
    with pytest.raises(UnsafeSqlError):
        quote_identifier("")


def test_string_literal_escapes_quotes():
    assert string_literal("it's") == "'it''s'"


def test_render_options_formats_each_type():
    options = {
        "all_varchar": True,
        "header": False,
        "skip": 2,
        "delim": ",",
        "nullstr": ["NA", ""],
    }

    assert render_options(options) == (
        "all_varchar = true, header = false, skip = 2, delim = ',', "
        "nullstr = ['NA', '']"
    )


def test_render_options_returns_empty_string_for_no_options():
    assert render_options({}) == ""


def test_render_options_rejects_unsafe_option_name():
    with pytest.raises(UnsafeSqlError):
        render_options({"x; DROP TABLE y": True})


def test_render_options_rejects_unsupported_value_type():
    with pytest.raises(UnsafeSqlError):
        render_options({"skip": None})
