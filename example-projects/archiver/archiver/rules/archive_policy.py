import logging
from collections.abc import Sequence

from archiver.rules.decision_resolver import ArchiveDecisionResolver
from archiver.rules.entities import ArchiveCandidate, ArchiveDecision, ResolvedArchiveDecision
from archiver.rules.ports import CandidateRule, CandidateSetRule

logger = logging.getLogger(__name__)


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
