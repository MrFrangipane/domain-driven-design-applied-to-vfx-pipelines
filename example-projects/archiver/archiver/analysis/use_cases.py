from pathlib import Path

from library_path import LibraryPath, LibraryPathError

from archiver.analysis.infrastructure.filesystem import FilesystemScanner
from archiver.archive.entities import ArchivePlan, ArchivePlanItem
from archiver.rules.entities import RuleContext
from archiver.rules.policies import FirstMatchingRulePolicy


class BuildArchivePlanUseCase:
    def __init__(
        self,
        library_path: LibraryPath,
        rule_policy: FirstMatchingRulePolicy,
        scanner: FilesystemScanner,
    ) -> None:
        self._scanner = scanner
        self._rule_policy = rule_policy
        self._library_path = library_path

    def execute(self, root: Path) -> ArchivePlan:
        plan_items: list[ArchivePlanItem] = []

        for source_path in self._scanner.walk_files(root):
            try:
                parsed_path = self._library_path.parse_path(source_path.as_posix())
            except LibraryPathError:
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
