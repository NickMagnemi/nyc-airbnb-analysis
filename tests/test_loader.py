from duckpipe.config import SourceConfig
from duckpipe.connection import open_database
from duckpipe.loader import TableLoader
from duckpipe.readers import reader_for


def test_open_database_without_path_is_in_memory():
    with open_database() as con:
        assert con.execute("SELECT 42").fetchone() == (42,)


def test_load_creates_table_from_every_matching_file(connection, tmp_path):
    (tmp_path / "items_a.csv").write_text("id,name\n1,first\n")
    (tmp_path / "items_b.csv").write_text("id,name\n2,second\n")
    source = SourceConfig(table="raw_items", path="items_*.csv", format="csv")

    TableLoader(connection, tmp_path).load(source, reader_for("csv"))

    assert connection.execute("SELECT COUNT(*) FROM raw_items").fetchone() == (2,)


def test_load_fills_filename_column_from_the_file_name(connection, tmp_path):
    (tmp_path / "items_2025-01-15.csv").write_text("id,name\n1,first\n2,second\n")
    source = SourceConfig(
        table="raw_items",
        path="items_*.csv",
        format="csv",
        filename_column="snapshot_date",
        filename_pattern=r"(\d{4}-\d{2}-\d{2})",
    )

    TableLoader(connection, tmp_path).load(source, reader_for("csv"))

    rows = connection.execute('SELECT DISTINCT "snapshot_date" FROM raw_items')
    assert rows.fetchall() == [("2025-01-15",)]
