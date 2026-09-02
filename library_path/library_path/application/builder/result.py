from dataclasses import dataclass
from pathlib import PurePosixPath


@dataclass(frozen=True)
class BuildPathResult:
    path: PurePosixPath

    @property
    def as_string(self) -> str:
        return self.path.as_posix()
