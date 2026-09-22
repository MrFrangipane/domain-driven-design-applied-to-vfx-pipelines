import logging
from collections.abc import Sequence

from archiver.planning.ports import ArchivePathBuilder
from archiver.rules.entities import ArchiveCandidate, ArchiveDecision, ArchiveMark, ResolvedArchiveDecision

logger = logging.getLogger(__name__)


class ArchiveDecisionResolver:
    """
    Resolves rule intent into final archive actions.

    Current conflict strategy:

    - A candidate is archived only if at least one rule marks it ARCHIVABLE.
    - A candidate is not archived if any rule marks it DO_NOT_ARCHIVE.
    - DO_NOT_ARCHIVE wins over ARCHIVABLE.
    """

    def __init__(self, archive_path_builder: ArchivePathBuilder) -> None:
        self._archive_path_builder = archive_path_builder

    def resolve(
        self,
        candidates: Sequence[ArchiveCandidate],
        decisions: Sequence[ArchiveDecision],
    ) -> Sequence[ResolvedArchiveDecision]:
        logger.debug(
            "Resolving archive decisions for %d candidates and %d rule decisions",
            len(candidates),
            len(decisions),
        )

        decisions_by_candidate: dict[ArchiveCandidate, list[ArchiveDecision]] = {
            candidate: [] for candidate in candidates
        }

        for decision in decisions:
            decisions_by_candidate.setdefault(decision.candidate, []).append(decision)

        resolved_decisions = [
            self._resolve_candidate(candidate, decisions_by_candidate[candidate])
            for candidate in candidates
        ]

        logger.debug("Resolved %d archive decisions", len(resolved_decisions))

        return resolved_decisions

    def _resolve_candidate(
        self,
        candidate: ArchiveCandidate,
        decisions: Sequence[ArchiveDecision],
    ) -> ResolvedArchiveDecision:
        has_archiveable_decision = any(
            decision.mark == ArchiveMark.ARCHIVABLE
            for decision in decisions
        )
        has_do_not_archive_decision = any(
            decision.mark == ArchiveMark.DO_NOT_ARCHIVE
            for decision in decisions
        )

        should_archive = has_archiveable_decision and not has_do_not_archive_decision
        archive_path = (
            self._archive_path_builder.build_archive_path(candidate)
            if should_archive
            else None
        )

        logger.debug(
            "Resolved candidate %r: should_archive=%s, has_archiveable_decision=%s, has_do_not_archive_decision=%s",
            candidate,
            should_archive,
            has_archiveable_decision,
            has_do_not_archive_decision,
        )

        return ResolvedArchiveDecision(
            candidate=candidate,
            should_archive=should_archive,
            archive_path=archive_path,
            reasons=tuple(
                decision.reason
                for decision in decisions
                if decision.reason
            ),
        )
