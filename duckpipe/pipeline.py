"""Runs the stages in order: extract, load, check, transform, export.

Pipeline only coordinates. Each stage's real work lives in its own class, which
Pipeline receives ready-made (dependency inversion). It never builds them.

build_pipeline is the one place that wires everything together. C# equivalent:
the service registrations in Program.cs, often called the "composition root".
"""

from collections.abc import Sequence
from dataclasses import dataclass

from duckpipe.checks import Check, CheckRunner
from duckpipe.config import PipelineConfig, SourceConfig
from duckpipe.connection import Connection
from duckpipe.extract import Downloader
from duckpipe.loader import TableLoader
from duckpipe.outputs import Output
from duckpipe.transforms import Transform


@dataclass(frozen=True)
class Pipeline:
    """One configured pipeline, ready to run."""

    sources: Sequence[SourceConfig]
    downloader: Downloader
    loader: TableLoader
    check_runner: CheckRunner
    checks: Sequence[tuple[str, Check]]  # (table, check) pairs
    transforms: Sequence[Transform]
    outputs: Sequence[Output]
    output_tables: Sequence[str]

    def run(self) -> None:
        """Run every stage in order, stopping at the first failed stage."""
        # TODO: call the five methods below in order, printing a short progress
        #       line before each. Keep this method as a readable table of contents.
        raise NotImplementedError

    def extract(self) -> None:
        """Download missing files for every source that lists downloads."""
        # TODO
        raise NotImplementedError

    def load(self) -> None:
        """Load every source into its raw table."""
        # TODO: self.loader.load(source, reader_for(source.format)) for each source.
        raise NotImplementedError

    def check(self) -> None:
        """Run all checks, print a summary, and stop if any failed."""
        # TODO: run_all, print one line per result, then raise_if_failed.
        raise NotImplementedError

    def transform(self) -> None:
        """Apply every transform in order."""
        # TODO
        raise NotImplementedError

    def export(self) -> None:
        """Send the output tables to every configured output."""
        # TODO
        raise NotImplementedError


def build_pipeline(config: PipelineConfig, connection: Connection) -> Pipeline:
    """Create every collaborator from `config` and return a Pipeline.

    This is the only function that knows about every concrete class.
    """
    # TODO: construct Downloader, TableLoader, CheckRunner; build each check with
    #       build_check, each transform as SqlFileTransform, each output with
    #       build_output. output_tables comes straight from config.output_tables.
    raise NotImplementedError
