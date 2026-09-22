from dataclasses import dataclass
from pathlib import PurePosixPath

from pipeline_path import Asset, EntityType, ParsedPath, Shot, WorkType


@dataclass(frozen=True)
class BrowserItem:
    """
    A pipeline path that can be displayed or filtered by the browser.

    This object belongs to the non-UI browser core. It does not know anything
    about Qt models, widgets, selections, or views.
    """

    path: PurePosixPath
    parsed_path: ParsedPath

    @property
    def project_code(self) -> str:
        return self.parsed_path.identity.project.code

    @property
    def entity_type(self) -> EntityType:
        if isinstance(self.parsed_path.identity.entity, Asset):
            return EntityType.ASSET

        return EntityType.SHOT

    @property
    def entity_name(self) -> str:
        if self.entity_type == EntityType.ASSET:
            return self.parsed_path.identity.entity.name
        else:
            return self.parsed_path.identity.entity.code

    @property
    def task_name(self) -> str:
        return self.parsed_path.identity.task.name

    @property
    def version_label(self) -> str:
        return self.parsed_path.identity.version.label

    @property
    def work_type(self) -> WorkType:
        return self.parsed_path.identity.work_type

    @property
    def extension(self) -> str:
        return self.parsed_path.extension


@dataclass(frozen=True)
class BrowserFilter:
    """
    Optional filter criteria for browser items.

    Any field left as None is ignored.
    """

    project_code: str | None = None
    entity_type: EntityType | None = None
    task_name: str | None = None
    work_type: WorkType | None = None
    extension: str | None = None
    search_text: str | None = None

    def matches(self, item: BrowserItem) -> bool:
        if self.project_code is not None and item.project_code != self.project_code:
            return False

        if self.entity_type is not None and item.entity_type is not self.entity_type:
            return False

        if self.task_name is not None and item.task_name != self.task_name:
            return False

        if self.work_type is not None and item.work_type is not self.work_type:
            return False

        if self.extension is not None and item.extension != self.extension:
            return False

        if self.search_text is not None:
            normalized_search_text = self.search_text.casefold()
            searchable_text = " ".join(
                [
                    item.path.as_posix(),
                    item.project_code,
                    item.entity_name,
                    item.task_name,
                    item.version_label,
                    item.work_type.value,
                    item.extension,
                ]
            ).casefold()

            if normalized_search_text not in searchable_text:
                return False

        return True
