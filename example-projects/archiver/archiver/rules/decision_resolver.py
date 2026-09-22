import logging
from collections.abc import Sequence

from archiver.archive.ports import ArchivePathBuilder
from archiver.rules.entities import ArchiveCandidate, ArchiveDecision, ArchiveMark, ResolvedArchiveDecision
from archiver.rules.ports import CandidateRule, CandidateSetRule

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


class ArchiveRulePolicy:
    """
    Coordinates rule evaluation.

    Rules express intent.
    The resolver decides the final action.
    """

    def __init__(
        self,
        candidate_rules: Sequence[CandidateRule],
        candidate_set_rules: Sequence[CandidateSetRule],
        resolver: ArchiveDecisionResolver,
    ) -> None:
        self._candidate_rules = tuple(candidate_rules)
        self._candidate_set_rules = tuple(candidate_set_rules)
        self._resolver = resolver

    def evaluate(
        self,
        candidates: Sequence[ArchiveCandidate],
    ) -> Sequence[ResolvedArchiveDecision]:
        logger.debug(
            "Evaluating archive policy for %d candidates using %d candidate rules and %d candidate set rules",
            len(candidates),
            len(self._candidate_rules),
            len(self._candidate_set_rules),
        )

        decisions: list[ArchiveDecision] = []

        for candidate in candidates:
            for rule in self._candidate_rules:
                decision = rule.evaluate(candidate)

                if decision is not None:
                    logger.debug(
                        "Candidate rule %s produced decision %r for candidate %r",
                        rule.__class__.__name__,
                        decision,
                        candidate,
                    )
                    decisions.append(decision)

        for rule in self._candidate_set_rules:
            rule_decisions = tuple(rule.evaluate(candidates))
            logger.debug(
                "Candidate set rule %s produced %d decisions",
                rule.__class__.__name__,
                len(rule_decisions),
            )
            decisions.extend(rule_decisions)

        logger.debug("Policy evaluation produced %d total rule decisions", len(decisions))

        return self._resolver.resolve(
            candidates=candidates,
            decisions=decisions,
        )
