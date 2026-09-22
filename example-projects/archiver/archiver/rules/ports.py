from collections.abc import Sequence
from typing import Protocol

from archiver.rules.entities import ArchiveCandidate, ArchiveDecision


class CandidateRule(Protocol):
    """
    Rule that evaluates one archive candidate.

    Example:
    - ArchiveWorkFilesRule
    """

    def evaluate(self, candidate: ArchiveCandidate) -> ArchiveDecision | None:
        ...


class CandidateSetRule(Protocol):
    """
    Rule that evaluates a collection of archive candidates.

    Example:
    - KeepLastThreeVersionsRule
    - KeepOneCachePerFrameRangeRule
    - KeepLatestPublishPerDepartmentRule
    """

    def evaluate(
        self,
        candidates: Sequence[ArchiveCandidate],
    ) -> Sequence[ArchiveDecision]:
        ...
