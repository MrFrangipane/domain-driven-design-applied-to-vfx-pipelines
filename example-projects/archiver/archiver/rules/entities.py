from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from library_path import ParsedPath


@dataclass(frozen=True)
class RuleContext:
    source_path: Path
    parsed_path: ParsedPath


@dataclass(frozen=True)
class RuleDecision:
    should_archive: bool
    archive_path: PurePosixPath | None = None
    reason: str = ""
