from pathlib import PurePosixPath

from library_path.application.build_path import BuildPathUseCase
from library_path.domain.entities import Asset, Project, Sequence, Shot, Task, Version, WorkType
from library_path.infrastructure.path_templates import PathTemplates


def build_shot_path(
    project: str,
    sequence: str,
    shot: str,
    task: str,
    version: int,
    work_type: WorkType | str,
    extension: str = "ma",
) -> PurePosixPath:
    """
    Public API for building a shot path.

    External tools such as browser or archiver can call this function without
    knowing how the library_path package is organized internally.
    """
    use_case = BuildPathUseCase(
        templates=PathTemplates.default_vfx_templates(),
    )

    return use_case.execute(
        project=Project(code=project),
        entity=Shot(
            sequence=Sequence(code=sequence),
            code=shot,
        ),
        task=Task(name=task),
        version=Version(number=version),
        work_type=WorkType(work_type),
        extension=extension,
    )


def build_asset_path(
    project: str,
    asset_type: str,
    asset: str,
    task: str,
    version: int,
    work_type: WorkType | str,
    extension: str = "ma",
) -> PurePosixPath:
    """
    Public API for building an asset path.
    """
    use_case = BuildPathUseCase(
        templates=PathTemplates.default_vfx_templates(),
    )

    return use_case.execute(
        project=Project(code=project),
        entity=Asset(
            asset_type=asset_type,
            name=asset,
        ),
        task=Task(name=task),
        version=Version(number=version),
        work_type=WorkType(work_type),
        extension=extension,
    )


__all__ = [
    "Asset",
    "Project",
    "Sequence",
    "Shot",
    "Task",
    "Version",
    "WorkType",
    "build_asset_path",
    "build_shot_path",
]
