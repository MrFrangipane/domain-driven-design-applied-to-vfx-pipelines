class PipelinePathError(Exception):
    """Base exception for the pipeline_path package."""


class InvalidPathDataError(PipelinePathError):
    """Raised when entities contain invalid path data."""


class PathTemplateNotFoundError(PipelinePathError):
    """Raised when no path template can be found for a requested use case."""


class PathParseError(PipelinePathError):
    """
    Raised when a filesystem path does not match any known pipeline path pattern.
    """
