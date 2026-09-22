from pathlib import Path
from typing import Iterable


class FilesystemScanner:
    def walk_files(self, root: Path) -> Iterable[Path]:
        if not root.exists():
            raise FileNotFoundError(f"Root folder does not exist: {root}")

        if not root.is_dir():
            raise NotADirectoryError(f"Root path is not a folder: {root}")

        for path in root.rglob("*"):
            if path.is_file():
                yield path
