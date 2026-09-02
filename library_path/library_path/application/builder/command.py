from dataclasses import dataclass

from library_path.domain.entities import Project, Shot, Asset, Task, Version, WorkType


@dataclass(frozen=True)
class BuildPathCommand:
    """
    Input DTO for the build-path use case.

    It intentionally contains domain entities.
    Validation belongs to the entities, not to infrastructure code.
    """

    project: Project
    entity: Shot | Asset
    task: Task
    version: Version
    work_type: WorkType
    extension: str = "ma"
