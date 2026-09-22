from pathlib import Path

from pipeline_path import PipelinePath, PipelinePathError

from archiver.analysis.infrastructure.filesystem import FilesystemScanner
from archiver.archive.entities import ArchivePlan, ArchivePlanItem
from archiver.rules.decision_resolver import ArchiveRulePolicy
from archiver.rules.entities import ArchiveCandidate


class BuildArchivePlanUseCase:
    def __init__(
        self,
        pipeline_path_api: PipelinePath,
        rule_policy: ArchiveRulePolicy,
        scanner: FilesystemScanner,
    ) -> None:
        self._scanner = scanner
        self._rule_policy = rule_policy
        self._pipeline_path_api = pipeline_path_api

    def execute(self, root: Path) -> ArchivePlan:
        candidates: list[ArchiveCandidate] = []

        for source_path in self._scanner.walk_files(root):
            try:
                parsed_path = self._pipeline_path_api.parse_path(source_path.as_posix())
            except PipelinePathError:
                continue

            candidates.append(
                ArchiveCandidate(
                    source_path=source_path,
                    parsed_path=parsed_path,
                )
            )

        resolved_decisions = self._rule_policy.evaluate(candidates)

        plan_items: list[ArchivePlanItem] = []

        for decision in resolved_decisions:
            if not decision.should_archive or decision.archive_path is None:
                continue

            plan_items.append(
                ArchivePlanItem(
                    source_path=decision.candidate.source_path,
                    archive_path=decision.archive_path,
                    reasons=decision.reasons,
                )
            )

        return ArchivePlan(items=tuple(plan_items))
