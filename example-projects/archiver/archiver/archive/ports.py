from pathlib import PurePosixPath
from typing import Protocol

from archiver.rules.entities import ArchiveCandidate


class ArchivePathBuilder(Protocol):
    """
    Builds the archive destination path for a candidate.

    This answers where an archivable candidate should be moved/copied to.
    """

    def build_archive_path(self, candidate: ArchiveCandidate) -> PurePosixPath:
        ...
