from collections.abc import Iterable
from pathlib import Path
from typing import Protocol


class FileScanner(Protocol):
    """
    Finds files that can be considered by the archiving use case.

    This is a port: the use case depends on this abstraction, not on a
    concrete filesystem implementation.
    """

    def walk_files(self, root: Path) -> Iterable[Path]:
        ...
