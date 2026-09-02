from pathlib import PurePosixPath

from library_path.application.builder.command import BuildPathCommand
from library_path.application.builder.path_renderer import PathRenderer
from library_path.application.builder.path_template_repository import PathTemplateRepository
from library_path.application.builder.result import BuildPathResult
from library_path.domain.entities import Shot


class BuildPathUseCase:
    def __init__(
        self,
        template_repository: PathTemplateRepository,
        renderer: PathRenderer,
    ) -> None:
        self._template_repository = template_repository
        self._renderer = renderer

    def execute(self, command: BuildPathCommand) -> BuildPathResult:
        template = self._template_repository.get_template(
            entity_type=command.entity.entity_type,
            work_type=command.work_type,
        )

        values = self._build_template_values(command)
        rendered_path = self._renderer.render(template, values)

        return BuildPathResult(path=PurePosixPath(rendered_path))

    def _build_template_values(self, command: BuildPathCommand) -> dict[str, object]:
        common_values: dict[str, object] = {
            "project": command.project.code,
            "task": command.task.name,
            "version": command.version.label,
            "version_number": command.version.number,
            "work_type": command.work_type.value,
            "extension": command.extension.lstrip("."),
        }

        if isinstance(command.entity, Shot):
            shot = command.entity

            return {
                **common_values,
                "entity_type": "shot",
                "sequence": shot.sequence.code,
                "shot": shot.code,
                "name": f"{command.project.code}_{shot.sequence.code}_{shot.code}_{command.task.name}",
            }

        asset = command.entity

        return {
            **common_values,
            "entity_type": "asset",
            "asset_type": asset.asset_type,
            "asset": asset.name,
            "name": f"{command.project.code}_{asset.asset_type}_{asset.name}_{command.task.name}",
        }

