from dataclasses import dataclass

from library_path.application.builder.path_template_repository import PathTemplateRepository
from library_path.domain.entities import EntityType, WorkType
from library_path.domain.exceptions import PathTemplateNotFoundError


@dataclass(frozen=True)
class InMemoryPathTemplateRepository(PathTemplateRepository):
    """
    Simple adapter useful for tests, examples, or local tools.

    In production, this could be replaced by:
    - YAMLPathTemplateRepository
    - JsonPathTemplateRepository
    - ShotGridPathTemplateRepository
    - DatabasePathTemplateRepository
    """

    templates: dict[tuple[EntityType, WorkType], str]

    @classmethod
    def with_default_vfx_templates(cls) -> "InMemoryPathTemplateRepository":
        return cls(
            templates={
                (
                    EntityType.SHOT,
                    WorkType.WORK,
                ): "/show/{project}/sequences/{sequence}/shots/{shot}/{task}/work/{version}/{name}_{version}.{extension}",
                (
                    EntityType.SHOT,
                    WorkType.PUBLISH,
                ): "/show/{project}/sequences/{sequence}/shots/{shot}/{task}/publish/{version}/{name}_{version}.{extension}",
                (
                    EntityType.ASSET,
                    WorkType.WORK,
                ): "/show/{project}/assets/{asset_type}/{asset}/{task}/work/{version}/{name}_{version}.{extension}",
                (
                    EntityType.ASSET,
                    WorkType.PUBLISH,
                ): "/show/{project}/assets/{asset_type}/{asset}/{task}/publish/{version}/{name}_{version}.{extension}",
            }
        )

    def get_template(self, entity_type: EntityType, work_type: WorkType) -> str:
        key = (entity_type, work_type)

        try:
            return self.templates[key]
        except KeyError as error:
            raise PathTemplateNotFoundError(
                f"No path template found for entity_type={entity_type.value!r}, work_type={work_type.value!r}."
            ) from error
