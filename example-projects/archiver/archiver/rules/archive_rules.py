from pathlib import PurePosixPath

from library_path import WorkType

from archiver.rules.entities import RuleContext, RuleDecision
from archiver.rules.ports import ArchiveRulePort


class ArchiveWorkFilesRule(ArchiveRulePort):
    def __init__(self, archive_root: str = "/archive") -> None:
        self._archive_root = PurePosixPath(archive_root)

    def evaluate(self, context: RuleContext) -> RuleDecision:
        if context.parsed_path.identity.work_type != WorkType.WORK:
            return RuleDecision(
                should_archive=False,
                reason="Only work files are archived.",
            )

        source_library_path = PurePosixPath(context.source_path.as_posix())

        if source_library_path.is_absolute():
            source_library_path = source_library_path.relative_to("/")

        archive_path = self._archive_root / source_library_path

        return RuleDecision(
            should_archive=True,
            archive_path=archive_path,
            reason="Work file matched archive policy.",
        )
