"""Downloads source files once, from trusted hosts only.

This is the "E" in ELT. It only runs for sources that list `downloads` in
pipeline.toml; local files that are already in data/ need nothing.

Security choices (carried over from the first project):
- HTTPS only, and only to hosts in allowed_hosts.
- File names can't contain folders, so nothing is written outside data_dir.
- Download to a .part file and rename when complete, so a half-finished
  download is never mistaken for real data.

Dependency inversion: the function that opens a URL is passed in, so tests can
hand in a fake that returns bytes without touching the internet.
"""

import urllib.request
from collections.abc import Callable, Collection, Mapping
from pathlib import Path
from typing import BinaryIO

DOWNLOAD_TIMEOUT_SECONDS = 60

type Opener = Callable[[str], BinaryIO]


def open_url(url: str) -> BinaryIO:
    """Open `url` for reading. The real Opener; tests use a fake one."""
    # Downloader._check_url has already allowed this URL.
    return urllib.request.urlopen(url, timeout=DOWNLOAD_TIMEOUT_SECONDS)  # noqa: S310


class Downloader:
    """Fetches any configured files that aren't in data_dir yet."""

    def __init__(
        self,
        data_dir: Path,
        allowed_hosts: Collection[str],
        opener: Opener = open_url,
    ) -> None:
        self._data_dir = data_dir
        self._allowed_hosts = frozenset(allowed_hosts)
        self._opener = opener

    def download_missing(self, downloads: Mapping[str, str]) -> list[Path]:
        """Download each file name -> URL pair not already saved; return new paths."""
        # TODO:
        # 1. Make sure data_dir exists (mkdir with parents=True, exist_ok=True).
        # 2. For each pair: check the name and URL, skip if the target exists,
        #    otherwise call self._download and collect the path.
        raise NotImplementedError

    def _check_url(self, url: str) -> str:
        """Return `url` if it's HTTPS to an allowed host; else UntrustedSourceError."""
        # TODO: urllib.parse.urlparse(url); check .scheme and .hostname.
        raise NotImplementedError

    @staticmethod
    def _check_file_name(file_name: str) -> str:
        """Return `file_name` if it has no folders in it; else UntrustedSourceError."""
        # TODO: Path(file_name).name must equal file_name, and it can't be empty.
        raise NotImplementedError

    def _download(self, url: str, target: Path) -> None:
        """Stream `url` into target.part, then rename it to `target`."""
        # TODO: `with self._opener(url) as response, partial.open("wb") as out:`
        #       then shutil.copyfileobj(response, out), then partial.rename(target).
        raise NotImplementedError
