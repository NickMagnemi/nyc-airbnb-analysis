"""Project settings: where files live and which tables to build"""

from pathlib import Path

DATA_DIR = Path("data")
DATABASE_PATH = Path("airbnb.duckdb")

# Table name -> file pattern. To load a new kind of file, add a line here.
SOURCES = {
    "raw_listings": "raw_listings_*.csv.gz"
} 

# File name -> download link from insideairbnb.com/get-the-data.
SNAPSHOT_URLS = {
    "listings_2026-09-14.csv.gz": "https://data.insideairbnb.com/united-states/ny/new-york-city/2026-09-14/data/listings.csv.gz",
}
