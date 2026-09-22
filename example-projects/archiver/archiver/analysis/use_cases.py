from pathlib import Path

from pipeline_path import PipelinePath, PipelinePathError

from archiver.analysis.infrastructure.filesystem import FilesystemScanner
from archiver.archive.entities import ArchivePlan, ArchivePlanItem
from archiver.rules.entities import RuleContext
from archiver.rules.policies import FirstMatchingRulePolicy


class BuildArchivePlanUseCase:
    def __init__(
        self,
        pipeline_path: PipelinePath,
        rule_policy: FirstMatchingRulePolicy,
        scanner: FilesystemScanner,
    ) -> None:
        self._scanner = scanner
        self._rule_policy = rule_policy
        self._pipeline_path = pipeline_path

    def execute(self, root: Path) -> ArchivePlan:
        plan_items: list[ArchivePlanItem] = []

        for source_path in self._scanner.walk_files(root):
            try:
                parsed_path = self._pipeline_path.parse_path(source_path.as_posix())
            except PipelinePathError:
                continue

            decision = self._rule_policy.evaluate(
                RuleContext(
                    source_path=source_path,
                    parsed_path=parsed_path,
                )
            )

            if not decision.should_archive or decision.archive_path is None:
                continue

            plan_items.append(
                ArchivePlanItem(
                    source_path=source_path,
                    archive_path=decision.archive_path,
                    reason=decision.reason,
                )
            )

        return ArchivePlan(items=tuple(plan_items))
