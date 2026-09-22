from dataclasses import dataclass
from enum import Enum
from pathlib import Path, PurePosixPath

from pipeline_path import ParsedPath


@dataclass(frozen=True)
class ArchiveCandidate:
    """
    A parsed file that may participate in archive rules.

    This replaces RuleContext. The candidate is the meaningful domain object
    passed to both single-candidate and collection rules.
    """

    source_path: Path
    parsed_path: ParsedPath


class ArchiveMark(str, Enum):
    """
    Intent expressed by a rule.

    Rules do not decide the final archive action. They only mark candidates.
    The resolver combines these marks into a final decision.
    """

    ARCHIVABLE = "archivable"
    DO_NOT_ARCHIVE = "do_not_archive"


@dataclass(frozen=True)
class ArchiveDecision:
    candidate: ArchiveCandidate
    mark: ArchiveMark
    reason: str


@dataclass(frozen=True)
class ResolvedArchiveDecision:
    candidate: ArchiveCandidate
    should_archive: bool
    archive_path: PurePosixPath | None
    reasons: tuple[str, ...]
