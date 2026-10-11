"""Project settings: where files live and which tables to build"""

from pathlib import Path

DATA_DIR = Path("data")
DATABASE_PATH = Path("airbnb.duckdb")

# Table name -> file pattern. To load a new kind of file, add a line here.
SOURCES = {
    "raw_listings": "raw_listings_*.csv.gz"
}