import pytest

from duckpipe.errors import ConfigError
from duckpipe.outputs import ParquetExport, PostgresSettings
from duckpipe.transforms import SqlFileTransform


def test_sql_file_transform_runs_every_statement(connection, tmp_path):
    sql_file = tmp_path / "build.sql"
    sql_file.write_text(
        "CREATE TABLE a AS SELECT 1 AS x;\nCREATE TABLE b AS SELECT 2 AS y;\n"
    )

    SqlFileTransform(sql_file).apply(connection)

    assert connection.execute("SELECT x FROM a").fetchone() == (1,)
    assert connection.execute("SELECT y FROM b").fetchone() == (2,)


def test_sql_file_transform_reports_a_missing_file(connection, tmp_path):
    with pytest.raises(ConfigError):
        SqlFileTransform(tmp_path / "missing.sql").apply(connection)


def test_parquet_export_writes_one_file_per_table(connection, tmp_path):
    connection.execute("CREATE TABLE items AS SELECT 1 AS id")

    ParquetExport(tmp_path / "exports").write(connection, ["items"])

    exported_file = tmp_path / "exports" / "items.parquet"
    exported = connection.execute(f"SELECT * FROM read_parquet('{exported_file}')")
    assert exported.fetchall() == [(1,)]


def test_postgres_settings_read_from_environment(monkeypatch):
    monkeypatch.setenv("POSTGRES_DB", "airbnb")
    monkeypatch.setenv("POSTGRES_USER", "tester")
    monkeypatch.setenv("POSTGRES_PASSWORD", "not-a-real-password")
    monkeypatch.delenv("POSTGRES_HOST", raising=False)

    settings = PostgresSettings.from_env()

    assert settings.host == "127.0.0.1"
    assert "user=tester" in settings.dsn()


def test_postgres_settings_report_missing_variables(monkeypatch):
    monkeypatch.delenv("POSTGRES_PASSWORD", raising=False)

    with pytest.raises(ConfigError):
        PostgresSettings.from_env()


def test_postgres_settings_never_show_the_password():
    settings = PostgresSettings("127.0.0.1", "5432", "airbnb", "tester", "s3cret")

    assert "s3cret" not in repr(settings)
