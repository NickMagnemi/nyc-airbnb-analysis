import io

import pytest

from duckpipe.errors import UntrustedSourceError
from duckpipe.extract import Downloader

ALLOWED = ["data.example.com"]
URL = "https://data.example.com/items.csv"


class FakeOpener:
    """Stands in for the internet: returns fixed bytes and records each URL."""

    def __init__(self, content=b"id\n1\n"):
        self.content = content
        self.urls = []

    def __call__(self, url):
        self.urls.append(url)
        return io.BytesIO(self.content)


def test_downloads_missing_file_without_leaving_a_part_file(tmp_path):
    opener = FakeOpener()

    new_files = Downloader(tmp_path, ALLOWED, opener).download_missing(
        {"items.csv": URL}
    )

    assert new_files == [tmp_path / "items.csv"]
    assert (tmp_path / "items.csv").read_bytes() == b"id\n1\n"
    assert not list(tmp_path.glob("*.part"))


def test_skips_files_that_already_exist(tmp_path):
    (tmp_path / "items.csv").write_text("already here")
    opener = FakeOpener()

    new_files = Downloader(tmp_path, ALLOWED, opener).download_missing(
        {"items.csv": URL}
    )

    assert new_files == []
    assert opener.urls == []


@pytest.mark.parametrize(
    "url",
    [
        "http://data.example.com/items.csv",
        "https://evil.example.org/items.csv",
        "file:///etc/passwd",
    ],
)
def test_rejects_untrusted_urls(tmp_path, url):
    downloader = Downloader(tmp_path, ALLOWED, FakeOpener())

    with pytest.raises(UntrustedSourceError):
        downloader.download_missing({"items.csv": url})
    assert not (tmp_path / "items.csv").exists()


@pytest.mark.parametrize("file_name", ["../outside.csv", "sub/items.csv", ""])
def test_rejects_file_names_with_folders(tmp_path, file_name):
    downloader = Downloader(tmp_path, ALLOWED, FakeOpener())

    with pytest.raises(UntrustedSourceError):
        downloader.download_missing({file_name: URL})
