from typing import Protocol

from library_path.domain.entities import EntityType, WorkType


class PathTemplateRepository(Protocol):
    """
    Port used by the application layer to retrieve path templates.

    Implementations may load templates from memory, YAML, JSON, a database,
    production tracking software, environment config, etc.
    """

    def get_template(self, entity_type: EntityType, work_type: WorkType) -> str:
        raise NotImplementedError
