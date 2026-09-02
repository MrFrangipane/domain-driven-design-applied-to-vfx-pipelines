from pathlib import PurePosixPath

from library_path.domain.entities import Asset, Project, Shot, Task, Version, WorkType
from library_path.domain.exceptions import InvalidPathDataError
from library_path.infrastructure.path_templates import PathTemplates


class BuildPathUseCase:
    """
    Application use case.

    This coordinates the workflow:
    - choose the right path template;
    - collect values from the domain objects;
    - render the final path.

    It does not know about Maya, Houdini, Qt, ShotGrid, databases, or files on disk.
    """

    def __init__(self, templates: PathTemplates) -> None:
        self._templates = templates

    def execute(
        self,
        project: Project,
        entity: Shot | Asset,
        task: Task,
        version: Version,
        work_type: WorkType,
        extension: str = "ma",
    ) -> PurePosixPath:
        template = self._templates.get_template(entity=entity, work_type=work_type)

        values = self._build_template_values(
            project=project,
            entity=entity,
            task=task,
            version=version,
            work_type=work_type,
            extension=extension,
        )

        return PurePosixPath(self._render(template, values))

    def _build_template_values(
        self,
        project: Project,
        entity: Shot | Asset,
        task: Task,
        version: Version,
        work_type: WorkType,
        extension: str,
    ) -> dict[str, object]:
        common_values: dict[str, object] = {
            "project": project.code,
            "task": task.name,
            "version": version.label,
            "version_number": version.number,
            "work_type": work_type.value,
            "extension": extension.lstrip("."),
        }

        if isinstance(entity, Shot):
            return {
                **common_values,
                "sequence": entity.sequence.code,
                "shot": entity.code,
                "name": f"{project.code}_{entity.sequence.code}_{entity.code}_{task.name}",
            }

        return {
            **common_values,
            "asset_type": entity.asset_type,
            "asset": entity.name,
            "name": f"{project.code}_{entity.asset_type}_{entity.name}_{task.name}",
        }

    def _render(self, template: str, values: dict[str, object]) -> str:
        try:
            return template.format(**values)
        except KeyError as error:
            missing_key = error.args[0]
            raise InvalidPathDataError(
                f"Cannot render path template. Missing value: {missing_key!r}."
            ) from error
