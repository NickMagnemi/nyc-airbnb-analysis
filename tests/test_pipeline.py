"""End-to-end test: the last one to pass, once every class works.

It builds a tiny project in a temporary folder (data, config, SQL transform)
and runs the whole pipeline on it, exactly as the command line would.
"""

import duckdb
import pytest

from duckpipe.config import load_config
from duckpipe.errors import CheckFailedError
from duckpipe.pipeline import build_pipeline

CONFIG = r"""
database = "test.duckdb"
data_dir = "data"
transforms = ["sql/clean.sql"]
output_tables = ["items"]

[[sources]]
table = "raw_items"
path = "items_*.csv"
format = "csv"
filename_column = "snapshot_date"
filename_pattern = '(\d{4}-\d{2}-\d{2})'
options = { all_varchar = true }

[[checks]]
table = "raw_items"
kind = "not_null"
column = "id"

[[outputs]]
kind = "parquet"
directory = "exports"
"""

CLEAN_SQL = """
CREATE OR REPLACE TABLE items AS
SELECT
    CAST(id AS INTEGER) AS id,
    name,
    CAST(snapshot_date AS DATE) AS snapshot_date
FROM raw_items;
"""


@pytest.fixture
def project(tmp_path):
    (tmp_path / "data").mkdir()
    (tmp_path / "sql").mkdir()
    (tmp_path / "sql" / "clean.sql").write_text(CLEAN_SQL)
    (tmp_path / "pipeline.toml").write_text(CONFIG)
    return tmp_path


def run_pipeline(project):
    config = load_config(project / "pipeline.toml")
    with duckdb.connect(str(config.database)) as connection:
        build_pipeline(config, connection).run()


def test_pipeline_loads_checks_transforms_and_exports(project):
    (project / "data" / "items_2025-01-15.csv").write_text("id,name\n1,a\n2,b\n")

    run_pipeline(project)

    exported = duckdb.sql(
        f"SELECT COUNT(*) FROM read_parquet('{project / 'exports' / 'items.parquet'}')"
    )
    assert exported.fetchone() == (2,)


def test_pipeline_stops_before_transforms_when_a_check_fails(project):
    (project / "data" / "items_2025-01-15.csv").write_text("id,name\n,a\n")

    with pytest.raises(CheckFailedError):
        run_pipeline(project)
    assert not (project / "exports").exists()
