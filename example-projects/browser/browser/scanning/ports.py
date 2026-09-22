from pathlib import PurePosixPath
from typing import Protocol


class PathScanner(Protocol):
    """
    Port for discovering file paths.

    Application code depends on this interface instead of depending directly
    on pathlib, os.walk, or another concrete filesystem implementation.
    """

    def scan(self, root: str | PurePosixPath) -> list[PurePosixPath]:
        raise NotImplementedError
