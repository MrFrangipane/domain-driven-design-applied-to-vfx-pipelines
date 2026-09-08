from archiver.rules.entities import RuleContext, RuleDecision
from archiver.rules.ports import ArchiveRulePort


class FirstMatchingRulePolicy:
    def __init__(self, rules: list[ArchiveRulePort]) -> None:
        self._rules = rules

    def evaluate(self, context: RuleContext) -> RuleDecision:
        for rule in self._rules:
            decision = rule.evaluate(context)

            if decision.should_archive:
                return decision

        return RuleDecision(
            should_archive=False,
            reason="No archive rule matched.",
        )
