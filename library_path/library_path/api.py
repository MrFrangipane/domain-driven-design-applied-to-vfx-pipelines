from pathlib import PurePosixPath

from library_path.application.build_path import BuildPathUseCase
from library_path.application.parse_path import ParsePathUseCase
from library_path.domain.entities import Asset, Project, Sequence, Shot, Task, Version, WorkType, ParsedPath
from library_path.infrastructure.path_templates import PathTemplates
from library_path.infrastructure.template_path_parser import TemplatePathParser


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


def parse_path(path: str | PurePosixPath) -> ParsedPath:
    """
    Public API for parsing a known library path back into domain data.
    """
    templates = PathTemplates.default_vfx_templates()

    use_case = ParsePathUseCase(
        parser=TemplatePathParser(templates=templates),
    )

    return use_case.execute(path=path)


__all__ = [
    "Asset",
    "ParsedPath",
    "Project",
    "Sequence",
    "Shot",
    "Task",
    "Version",
    "WorkType",
    "build_asset_path",
    "build_shot_path",
    "parse_path",
]
