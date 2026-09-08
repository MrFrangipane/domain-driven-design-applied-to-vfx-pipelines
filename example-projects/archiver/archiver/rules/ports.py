from abc import ABC, abstractmethod

from archiver.rules.entities import RuleContext, RuleDecision


class ArchiveRulePort(ABC):
    """
    Port for archive rules.

    Implementations decide whether a parsed file should be archived.
    """

    @abstractmethod
    def evaluate(self, context: RuleContext) -> RuleDecision:
        raise NotImplementedError
