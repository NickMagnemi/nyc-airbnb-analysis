"""Download any configured snapshots that aren't saved yet."""

from airbnb.config import DATA_DIR, SNAPSHOT_URLS
from airbnb.download import download_missing


def main() -> None:
    new_files = download_missing(SNAPSHOT_URLS, DATA_DIR)
    print(f"Downloaded {len(new_files)} new file(s) into {DATA_DIR}/")


if __name__ == "__main__":
    main()