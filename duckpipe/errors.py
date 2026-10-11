"""Exceptions raised by duckpipe.

One base class lets callers catch every pipeline failure with a single
`except PipelineError`, while the subclasses say exactly what went wrong.
C# equivalent: a custom exception hierarchy deriving from Exception.

These are complete; nothing to implement here.
"""


class PipelineError(Exception):
    """Base class for every error duckpipe raises on purpose."""


class ConfigError(PipelineError):
    """pipeline.toml is missing a setting or contains an invalid one."""


class UnsafeSqlError(PipelineError):
    """A name or value could not be placed into SQL safely."""


class UntrustedSourceError(PipelineError):
    """A download URL or file name failed the security checks."""


class CheckFailedError(PipelineError):
    """One or more data quality checks failed."""
