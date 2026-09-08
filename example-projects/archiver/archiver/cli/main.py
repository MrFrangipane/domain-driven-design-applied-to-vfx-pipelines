import argparse
import json
from pathlib import Path

from library_path import LibraryPath

from archiver.analysis.infrastructure.filesystem import FilesystemScanner
from archiver.analysis.use_cases import BuildArchivePlanUseCase
from archiver.rules.policies import ArchiveWorkFilesRule, FirstMatchingRulePolicy


def build_archive_plan_use_case() -> BuildArchivePlanUseCase:
    rule_policy = FirstMatchingRulePolicy(
        rules=[
            ArchiveWorkFilesRule(archive_root="/archive"),
        ]
    )

    return BuildArchivePlanUseCase(
        library_path=LibraryPath.default(),
        rule_policy=rule_policy,
        scanner=FilesystemScanner(),
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="archiver",
        description="Build an archive plan for files matching library_path templates.",
    )
    parser.add_argument(
        "root",
        type=Path,
        help="Root folder to scan.",
    )

    args = parser.parse_args()

    use_case = build_archive_plan_use_case()
    plan = use_case.execute(args.root)

    payload = {
        "count": plan.count,
        "items": [
            {
                "source_path": item.source_path.as_posix(),
                "archive_path": item.archive_path.as_posix(),
                "reason": item.reason,
            }
            for item in plan.items
        ],
    }

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
