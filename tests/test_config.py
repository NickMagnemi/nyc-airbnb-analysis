import pytest

from duckpipe.config import CheckConfig, load_config
from duckpipe.errors import ConfigError

EXAMPLE = r"""
database = "test.duckdb"
data_dir = "data"
allowed_hosts = ["data.example.com"]
transforms = ["sql/clean.sql"]
output_tables = ["items"]

[[sources]]
table = "raw_items"
path = "items_*.csv"
format = "csv"
filename_column = "snapshot_date"
filename_pattern = '(\d{4}-\d{2}-\d{2})'
options = { all_varchar = true }

[sources.downloads]
"items_2025-01-15.csv" = "https://data.example.com/items.csv"

[[checks]]
table = "raw_items"
kind = "not_null"
column = "id"

[[outputs]]
kind = "parquet"
directory = "exports"
"""


def write_config(tmp_path, text):
    path = tmp_path / "pipeline.toml"
    path.write_text(text)
    return path


def test_load_config_reads_sources(tmp_path):
    config = load_config(write_config(tmp_path, EXAMPLE))

    (source,) = config.sources
    assert source.table == "raw_items"
    assert source.format == "csv"
    assert source.options == {"all_varchar": True}
    assert source.filename_pattern == r"(\d{4}-\d{2}-\d{2})"
    assert source.downloads == {
        "items_2025-01-15.csv": "https://data.example.com/items.csv"
    }


def test_load_config_makes_paths_relative_to_the_config_file(tmp_path):
    config = load_config(write_config(tmp_path, EXAMPLE))

    assert config.database == tmp_path / "test.duckdb"
    assert config.data_dir == tmp_path / "data"
    assert config.transforms == (tmp_path / "sql" / "clean.sql",)


def test_load_config_puts_extra_check_settings_in_params(tmp_path):
    config = load_config(write_config(tmp_path, EXAMPLE))

    assert config.checks == (
        CheckConfig(table="raw_items", kind="not_null", params={"column": "id"}),
    )


def test_load_config_rejects_unknown_format(tmp_path):
    text = EXAMPLE.replace('format = "csv"', 'format = "pdf"')

    with pytest.raises(ConfigError):
        load_config(write_config(tmp_path, text))


def test_load_config_requires_pattern_with_filename_column(tmp_path):
    text = EXAMPLE.replace("filename_pattern = '(\\d{4}-\\d{2}-\\d{2})'\n", "")

    with pytest.raises(ConfigError):
        load_config(write_config(tmp_path, text))


def test_load_config_turns_bad_toml_into_config_error(tmp_path):
    with pytest.raises(ConfigError):
        load_config(write_config(tmp_path, "database = "))
