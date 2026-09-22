import argparse
import json
from pathlib import Path, PurePosixPath

from pipeline_path import PipelinePath

from archiver.planning.path_builders import DefaultArchivePathBuilder
from archiver.rules.archive_rules import ArchiveWorkFilesRule, KeepLastVersionsRule
from archiver.rules.decision_resolver import ArchiveDecisionResolver, ArchiveRulePolicy
from archiver.scanning.filesystem import FilesystemScanner
from archiver.scanning.use_cases import BuildArchivePlanUseCase


def build_archive_plan_use_case() -> BuildArchivePlanUseCase:
    rule_policy = ArchiveRulePolicy(
        candidate_rules=[
            ArchiveWorkFilesRule(),
        ],
        candidate_set_rules=[
            KeepLastVersionsRule(
                number_of_versions_to_keep=2
            ),
        ],
        resolver=ArchiveDecisionResolver(
            archive_path_builder=DefaultArchivePathBuilder(
                archive_root=PurePosixPath("archives"),
            ),
        ),
    )

    return BuildArchivePlanUseCase(
        pipeline_path_api=PipelinePath.default(),
        rule_policy=rule_policy,
        scanner=FilesystemScanner(),
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="archiver",
        description="Build an archive plan for files matching pipeline_path templates.",
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
                "reasons": item.reasons,
            }
            for item in plan.items
        ],
    }

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    # import logging
    # logging.basicConfig(level=logging.DEBUG)
    main()
