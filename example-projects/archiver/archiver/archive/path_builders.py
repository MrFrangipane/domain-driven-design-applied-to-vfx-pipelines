from pathlib import PurePosixPath

from archiver.rules.entities import ArchiveCandidate


class DefaultArchivePathBuilder:
    """
    Builds archive destination paths.

    The current policy preserves the source filename and places it under
    the configured archive root.
    """

    def __init__(self, archive_root: PurePosixPath) -> None:
        self._archive_root = archive_root

    def build_archive_path(self, candidate: ArchiveCandidate) -> PurePosixPath:
        return self._archive_root / candidate.source_path
