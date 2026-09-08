from pathlib import PurePosixPath

from library_path.application.build_path import BuildPathUseCase
from library_path.application.parse_path import ParsePathUseCase
from library_path.domain.entities import (
    Asset,
    ParsedPath,
    Project,
    Sequence,
    Shot,
    Task,
    TaskVersionIdentity,
    Version,
    WorkType,
)
from library_path.infrastructure.path_templates import PathTemplates
from library_path.infrastructure.template_path_parser import TemplatePathParser


class LibraryPath:
    """
    Public API for building and parsing library paths.

    External tools can create one configured instance and reuse it instead of
    constructing use cases for every operation.
    """

    def __init__(self, templates: PathTemplates) -> None:
        self._build_path_use_case = BuildPathUseCase(templates=templates)
        self._parse_path_use_case = ParsePathUseCase(
            parser=TemplatePathParser(templates=templates),
        )

    @classmethod
    def default(cls) -> "LibraryPath":
        return cls(
            templates=PathTemplates.default_vfx_templates(),
        )

    @classmethod
    def from_templates(cls, templates: PathTemplates) -> "LibraryPath":
        return cls(templates=templates)

    def build_shot_path(
        self,
        project: str,
        sequence: str,
        shot: str,
        task: str,
        version: int,
        work_type: WorkType | str,
        extension: str,
    ) -> PurePosixPath:
        return self._build_path_use_case.execute(
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
        self,
        project: str,
        asset_type: str,
        asset: str,
        task: str,
        version: int,
        work_type: WorkType | str,
        extension: str,
    ) -> PurePosixPath:
        return self._build_path_use_case.execute(
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

    def parse_path(self, path: str | PurePosixPath) -> ParsedPath:
        return self._parse_path_use_case.execute(path=path)


__all__ = [
    "Asset",
    "LibraryPath",
    "ParsedPath",
    "Project",
    "Sequence",
    "Shot",
    "Task",
    "TaskVersionIdentity",
    "Version",
    "WorkType",
]
