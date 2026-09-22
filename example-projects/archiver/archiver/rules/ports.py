from typing import Protocol, Sequence

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
