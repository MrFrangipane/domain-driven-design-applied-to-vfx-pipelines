import re
from dataclasses import dataclass
from pathlib import PurePosixPath

from library_path.domain.entities import WorkType, EntityType
from library_path.infrastructure.path_templates import PathTemplates


@dataclass(frozen=True)
class ParsedTemplateValues:
    """
    Raw values captured from a path template.

    These are still plain strings. The application layer will turn them into
    domain objects such as Project, Shot, Asset, Task, and Version.
    """

    entity_type: EntityType
    work_type: WorkType
    values: dict[str, str]


class TemplatePathParser:
    """
    Infrastructure service.

    This class knows the technical details of matching filesystem paths against
    path templates. The application layer does not need to know that this uses
    regular expressions internally.
    """

    def __init__(self, templates: PathTemplates) -> None:
        self._templates = templates

    def parse(self, path: str | PurePosixPath) -> ParsedTemplateValues | None:
        path_text = PurePosixPath(path).as_posix()

        for work_type, template in self._templates.shot_templates.items():
            values = self._match_template(template=template, path=path_text)
            if values is not None:
                return ParsedTemplateValues(
                    entity_type=EntityType.SHOT,
                    work_type=work_type,
                    values=values,
                )

        for work_type, template in self._templates.asset_templates.items():
            values = self._match_template(template=template, path=path_text)
            if values is not None:
                return ParsedTemplateValues(
                    entity_type=EntityType.ASSET,
                    work_type=work_type,
                    values=values,
                )

        return None

    def _match_template(self, template: str, path: str) -> dict[str, str] | None:
        pattern = self._template_to_regex(template)
        match = re.fullmatch(pattern, path)

        if match is None:
            return None

        return match.groupdict()

    def _template_to_regex(self, template: str) -> str:
        field_patterns = {
            "project": r"[^/]+",
            "sequence": r"[^/]+",
            "shot": r"[^/]+",
            "asset_type": r"[^/]+",
            "asset": r"[^/]+",
            "task": r"[^/]+",
            "version": r"v\d+",
            "name": r"[^/]+",
            "extension": r"[^/.]+",
        }

        seen_fields: set[str] = set()

        def replace_field(match: re.Match[str]) -> str:
            field_name = match.group(1)

            if field_name not in field_patterns:
                return re.escape(match.group(0))

            if field_name in seen_fields:
                return rf"(?P={field_name})"

            seen_fields.add(field_name)
            return rf"(?P<{field_name}>{field_patterns[field_name]})"

        return re.sub(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", replace_field, template)
