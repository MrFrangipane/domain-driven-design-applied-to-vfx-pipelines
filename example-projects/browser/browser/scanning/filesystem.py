from pathlib import Path, PurePosixPath

from browser.scanning.ports import PathScanner


class FilesystemPathScanner(PathScanner):
    """
    Real filesystem implementation of PathScanner.
    """

    def scan(self, root: str | PurePosixPath) -> list[PurePosixPath]:
        root_path = Path(root)

        if not root_path.exists():
            return []

        if root_path.is_file():
            return [PurePosixPath(root_path.as_posix())]

        discovered_paths: list[PurePosixPath] = []

        for path in root_path.rglob("*"):
            if path.is_file():
                discovered_paths.append(PurePosixPath(path.as_posix()))

        return sorted(discovered_paths)
