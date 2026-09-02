from dataclasses import dataclass

from library_path.domain.entities import Asset, Shot, WorkType
from library_path.domain.exceptions import PathTemplateNotFoundError


@dataclass(frozen=True)
class PathTemplates:
    """
    Infrastructure detail.

    In this intro example, templates are stored in memory.

    In a real studio, this could be replaced with templates loaded from:
    - YAML;
    - JSON;
    - ShotGrid;
    - Kitsu;
    - Ftrack;
    - A database;
    - A central pipeline configuration package.
    """

    shot_templates: dict[WorkType, str]
    asset_templates: dict[WorkType, str]

    @classmethod
    def default_vfx_templates(cls) -> "PathTemplates":
        """
        Generates default visual effects (VFX) path templates for shots and assets.

        :rtype: PathTemplates
        :return: An instance of `PathTemplates` configured with default VFX shot and
                 asset path templates for both work-in-progress and published files.
        """
        return cls(
            shot_templates={
                WorkType.WORK: (
                    "/show/{project}/sequences/{sequence}/shots/{shot}/"
                    "{task}/work/{version}/{name}_{version}.{extension}"
                ),
                WorkType.PUBLISH: (
                    "/show/{project}/sequences/{sequence}/shots/{shot}/"
                    "{task}/publish/{version}/{name}_{version}.{extension}"
                ),
            },
            asset_templates={
                WorkType.WORK: (
                    "/show/{project}/assets/{asset_type}/{asset}/"
                    "{task}/work/{version}/{name}_{version}.{extension}"
                ),
                WorkType.PUBLISH: (
                    "/show/{project}/assets/{asset_type}/{asset}/"
                    "{task}/publish/{version}/{name}_{version}.{extension}"
                ),
            },
        )

    def get_template(self, entity: Shot | Asset, work_type: WorkType) -> str:
        if isinstance(entity, Shot):
            templates = self.shot_templates
            entity_name = "shot"
        else:
            templates = self.asset_templates
            entity_name = "asset"

        try:
            return templates[work_type]
        except KeyError as error:
            raise PathTemplateNotFoundError(
                f"No path template found for entity={entity_name!r}, work_type={work_type.value!r}."
            ) from error
