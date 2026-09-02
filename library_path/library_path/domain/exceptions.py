class LibraryPathError(Exception):
    """Base exception for the library_path package."""


class InvalidPathDataError(LibraryPathError):
    """Raised when entities contain invalid path data."""


class PathTemplateNotFoundError(LibraryPathError):
    """Raised when no path template can be found for a requested use case."""
