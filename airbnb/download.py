"""Download Inside Airbnb snapshot files once, skipping any already saved."""

import shutil
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_HOST = "data.insideairbnb.com"


def check_url(url: str) -> str:
    """Return `url` if it's an HTTPS Inside Airbnb link, else raise ValueError."""
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != ALLOWED_HOST:
        raise ValueError(f"Refusing to download from untrusted URL: {url}")
    return url


def check_file_name(file_name: str) -> str:
    """Return `file_name` if it's a plain name, not a path outside data/."""
    if Path(file_name).name != file_name:
        raise ValueError(f"File name must not contain folders: {file_name}")
    return file_name


def download_missing(urls: dict[str, str], data_dir: Path) -> list[Path]:
    """Download each file in `urls` that isn't in `data_dir` yet; return new paths."""
    data_dir.mkdir(exist_ok=True)
    downloaded: list[Path] = []
    for file_name, url in urls.items():
        target = data_dir / check_file_name(file_name)
        if target.exists():
            continue
        partial = target.with_name(target.name + ".part")
        with urllib.request.urlopen(check_url(url), timeout=60) as response:  # noqa: S310
            with partial.open("wb") as out:
                shutil.copyfileobj(response, out)
        partial.rename(target)
        downloaded.append(target)
    return downloaded