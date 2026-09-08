from dataclasses import dataclass
from pathlib import Path, PurePosixPath


@dataclass(frozen=True)
class ArchivePlanItem:
    source_path: Path
    archive_path: PurePosixPath
    reason: str


@dataclass(frozen=True)
class ArchivePlan:
    items: tuple[ArchivePlanItem, ...]

    @property
    def count(self) -> int:
        return len(self.items)
