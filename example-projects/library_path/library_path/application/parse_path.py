from pathlib import PurePosixPath

from library_path.domain.entities import (
    Asset,
    ParsedPath,
    Project,
    Sequence,
    Shot,
    Task,
    Version,
    WorkType, EntityType,
)
from library_path.domain.exceptions import PathParseError
from library_path.infrastructure.template_path_parser import TemplatePathParser


class ParsePathUseCase:
    """
    Application use case for parsing a filesystem path into domain data.

    This coordinates the workflow:
    - ask infrastructure to match the path against known templates;
    - convert the parsed values into domain objects.

    It does not know how the path is matched internally.
    """

    def __init__(self, parser: TemplatePathParser) -> None:
        self._parser = parser

    def execute(self, path: str | PurePosixPath) -> ParsedPath:
        parsed_values = self._parser.parse(path)

        if parsed_values is None:
            path_text = PurePosixPath(path).as_posix()
            raise PathParseError(f"Path does not match any known template: {path_text!r}.")

        if parsed_values.entity_type == EntityType.SHOT:
            return self._build_shot_result(
                values=parsed_values.values,
                work_type=parsed_values.work_type,
            )

        if parsed_values.entity_type == EntityType.ASSET:
            return self._build_asset_result(
                values=parsed_values.values,
                work_type=parsed_values.work_type,
            )

        raise PathParseError(f"Path does not match any known Entity Type: {parsed_values.entity_type}.")

    def _build_shot_result(self, values: dict[str, str], work_type: WorkType) -> ParsedPath:
        return ParsedPath(
            project=Project(code=values["project"]),
            entity=Shot(
                sequence=Sequence(code=values["sequence"]),
                code=values["shot"],
            ),
            task=Task(name=values["task"]),
            version=Version(number=self._parse_version_number(values["version"])),
            work_type=work_type,
            extension=values["extension"],
        )

    def _build_asset_result(self, values: dict[str, str], work_type: WorkType) -> ParsedPath:
        return ParsedPath(
            project=Project(code=values["project"]),
            entity=Asset(
                asset_type=values["asset_type"],
                name=values["asset"],
            ),
            task=Task(name=values["task"]),
            version=Version(number=self._parse_version_number(values["version"])),
            work_type=work_type,
            extension=values["extension"],
        )

    def _parse_version_number(self, version_label: str) -> int:
        return int(version_label.removeprefix("v"))
