from collections import defaultdict
from collections.abc import Sequence

from pipeline_path import VersionFamilyKey, WorkType

from archiver.rules.entities import ArchiveCandidate, ArchiveDecision, ArchiveMark


class ArchiveWorkFilesRule:
    """
    Single rule.

    Matches only files of the Work type.
    """
    def evaluate(self, candidate: ArchiveCandidate) -> ArchiveDecision | None:
        if candidate.parsed_path.identity.work_type != WorkType.WORK:
            return ArchiveDecision(
                candidate=candidate,
                mark=ArchiveMark.DO_NOT_ARCHIVE,
                reason="Is not of Work type",
            )

        return ArchiveDecision(
            candidate=candidate,
            mark=ArchiveMark.ARCHIVABLE,
            reason="Is of Work type",
        )


class KeepLastVersionsRule:
    """
    Collection rule.

    Groups candidates by VersionFamilyKey and protects the latest three versions
    in each family.
    """
    def __init__(self, number_of_versions_to_keep):
        self.number_of_versions_to_keep = number_of_versions_to_keep

    def evaluate(
        self,
        candidates: Sequence[ArchiveCandidate],
    ) -> Sequence[ArchiveDecision]:
        by_family: dict[VersionFamilyKey, list[ArchiveCandidate]] = defaultdict(list)

        for candidate in candidates:
            by_family[candidate.parsed_path.identity.version_family_key].append(candidate)

        decisions: list[ArchiveDecision] = []

        for family_candidates in by_family.values():
            candidates_sorted_by_version = sorted(
                family_candidates,
                key=lambda candidate_: candidate_.parsed_path.identity.version.number,
            )

            for candidate_to_exclude in candidates_sorted_by_version[:-self.number_of_versions_to_keep]:
                decisions.append(
                    ArchiveDecision(
                        candidate=candidate_to_exclude,
                        mark=ArchiveMark.DO_NOT_ARCHIVE,
                        reason=f"Not in the latest {self.number_of_versions_to_keep} versions in its version family.",
                    )
                )

            for candidate_to_keep in candidates_sorted_by_version[-self.number_of_versions_to_keep:]:
                decisions.append(
                    ArchiveDecision(
                        candidate=candidate_to_keep,
                        mark=ArchiveMark.ARCHIVABLE,
                        reason=f"One of the latest {self.number_of_versions_to_keep} versions in its version family.",
                    )
                )

        return decisions
