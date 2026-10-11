# Requirements

Each requirement is short, numbered and testable. "Covered by" says where it's implemented and which tests prove it, so every line can be traced from requirement to code.

## Problem statement

Analysts often rewrite the same loading code for every new dataset. duckpipe extracts and loads any file DuckDB can read and checks the raw data, all driven by one config file, so a new dataset needs configuration rather than new Python. dbt then transforms and tests the data, so the cleaning logic is versioned, tested SQL. duckpipe can also run simple SQL transforms and exports itself, for projects that don't use dbt.

The first project built on it analyses how Airbnb in New York City changed after Local Law 18, which began enforcement in September 2023.

## Users

| ID | User | What they need |
| --- | --- | --- |
| U1 | An analyst setting up a dataset (me) | Load, check and clean new data without writing new Python |
| U2 | A reviewer or hiring manager | Read the code, rebuild the results with one command, trust the findings |
| U3 | A future user of duckpipe | Add a file format, check or output without editing existing classes |

## Business questions (NYC Airbnb)

1. Did listings shift from short stays to 30+ night minimums after September 2023?
2. Did entire-home listings shrink compared with private rooms?
3. Did hosts with several listings leave the market, or adapt?
4. Which boroughs and neighbourhoods changed most?
5. What drives price today: area, room type, size or ratings?

## Functional requirements

### duckpipe

| ID | Requirement | Covered by |
| --- | --- | --- |
| FR1 | Read all pipeline settings from a TOML file, and reject missing or invalid settings with a clear message before any data is touched. | `config.py`; `test_config.py` |
| FR2 | Download each configured file once, only over HTTPS from an allowed host, and skip files already saved. | `extract.py`; `test_extract.py` |
| FR3 | Load every file matching a source's pattern into one raw table, unchanged, for CSV, Parquet, JSON and Excel. | `readers.py`, `loader.py`; `test_readers.py`, `test_loader.py` |
| FR4 | Optionally add a column to a raw table whose value is taken from each file's name, such as a snapshot date. | `loader.py`; `test_loader.py` |
| FR5 | Provide these data quality checks: required columns, no nulls in a column, unique values across columns, and a minimum row count overall or per group. | `checks.py`; `test_checks.py` |
| FR6 | Run every configured check, report each result, and stop before transforming if any check fails. | `checks.py`, `pipeline.py`; `test_checks.py`, `test_pipeline.py` |
| FR7 | For projects without dbt, run configured SQL transform files in the order listed. | `transforms.py`; `test_transforms_and_outputs.py` |
| FR8 | For projects without dbt, export chosen tables to Parquet files, and optionally to PostgreSQL. | `outputs.py`; `test_transforms_and_outputs.py` |
| FR9 | Run the whole pipeline with one command, `python -m duckpipe pipeline.toml`, exiting with code 0 on success and 1 on a handled failure. | `__main__.py`, `pipeline.py`; `test_pipeline.py` |
| FR10 | Produce the same result when run twice on the same data (idempotent). | `loader.py` (`CREATE OR REPLACE`); `test_pipeline.py` |

### NYC Airbnb analysis

| ID | Requirement | Covered by |
| --- | --- | --- |
| FR11 | Build a clean, typed `stg_listings` dbt model with personal fields removed, read from the raw table duckpipe loaded. | `dbt/models/staging/` |
| FR12 | Test the dbt models with dbt tests, such as no nulls in key columns. | `dbt/models/staging/_stg_listings.yml`; `dbt build` |
| FR13 | Answer each business question with one dbt mart model and one chart. | `dbt/models/marts/`, notebook |
| FR14 | Rebuild everything with one command: load and check with duckpipe, then `dbt build`. | `scripts/build.sh` |
| FR15 | Summarise the findings, with charts and caveats, in the README. | `README.md` |

## Non-functional requirements

| ID | Requirement | Covered by |
| --- | --- | --- |
| NFR1 | **Security, SQL injection:** values are always query parameters; table names are validated against an allowlist; names from data files are quoted and escaped. | `sql_safety.py`; `test_sql_safety.py`; Ruff `S608` |
| NFR2 | **Security, secrets:** no password or key is ever in the repository, the config file or an error message. Secrets live in `.env`. | `.gitignore`, `outputs.py`; secret scanning, push protection, gitleaks |
| NFR3 | **Privacy:** raw data and personal fields are never committed or published; published results are aggregates only, and Inside Airbnb is credited. | `.gitignore`, `stg_listings.sql`, nbstripout |
| NFR4 | **Reproducibility:** after cloning, one install command and one run command rebuild everything from scratch, using pinned versions of every dependency, including dbt. | `requirements.txt`, `scripts/build.sh`, README |
| NFR5 | **Extensibility:** a new file format, check or output can be added without changing existing classes. | Registries in `readers.py`, `checks.py`, `outputs.py` |
| NFR6 | **Testability:** every module has unit tests that need no network access and no real data files. | `tests/` |
| NFR7 | **Code quality:** the code passes Ruff with no warnings, and every public function has type hints and a docstring. | `pyproject.toml`; CI |
| NFR8 | **Performance:** loading and checking one full NYC snapshot (tens of thousands of listings) takes under one minute on a laptop. | Measured manually |
| NFR9 | **Usability:** every error message says what went wrong and how to fix it. | `errors.py`; tests that expect specific errors |

## Out of scope

- Scheduled or automatic runs: the pipeline runs when someone runs it.
- Incremental loads: each run rebuilds the tables from all files.
- A web interface or live dashboard.
- Streaming data, and databases other than DuckDB and PostgreSQL.

## Features (GitHub Issues)

Each feature is one GitHub Issue, one branch and one pull request. A feature is done when its tests pass, Ruff is clean, and it has been reviewed.

| # | Feature | Requirements | Done when |
| --- | --- | --- | --- |
| 1 | SQL safety helpers | NFR1 | `test_sql_safety.py` passes |
| 2 | Database connection | NFR6 | `open_database` test in `test_loader.py` passes |
| 3 | Pipeline configuration | FR1, NFR9 | `test_config.py` passes |
| 4 | File readers | FR3, NFR5 | `test_readers.py` passes |
| 5 | Raw table loader | FR3, FR4, FR10 | `test_loader.py` passes |
| 6 | Data quality checks | FR5, FR6 | `test_checks.py` passes |
| 7 | Safe downloads | FR2, NFR2 | `test_extract.py` passes |
| 8 | SQL transforms and exports | FR7, FR8, NFR2 | `test_transforms_and_outputs.py` passes |
| 9 | Pipeline and command line | FR6, FR9 | `test_pipeline.py` passes |
| 10 | Tests, linting and CI on every pull request | NFR4, NFR6, NFR7 | CI passes and is required on `main` |
| 11 | dbt project and staging model | FR11, FR12, NFR3 | `dbt build` creates `stg_listings` and its tests pass |
| 12 | One-command build | FR14, NFR4 | `scripts/build.sh` rebuilds everything from the raw files |
| 13 | Mart models for the business questions | FR13 | One mart model and chart per question |
| 14 | README write-up | FR15, NFR3, NFR4 | A stranger can rebuild and read the findings |
