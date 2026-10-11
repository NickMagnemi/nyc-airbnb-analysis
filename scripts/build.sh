#!/usr/bin/env bash
# Rebuild everything from the raw files: duckpipe loads and checks, then dbt
# transforms and tests. Run from the project root: ./scripts/build.sh
#
# These are two separate steps on purpose: DuckDB lets only one program write
# to airbnb.duckdb at a time, so duckpipe must finish (and close the file)
# before dbt opens it.

set -euo pipefail  # stop at the first failing command

python -m duckpipe pipeline.toml
dbt build --project-dir dbt --profiles-dir dbt
