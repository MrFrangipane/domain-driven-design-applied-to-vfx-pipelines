from dataclasses import dataclass
from enum import StrEnum

from library_path.domain.exceptions import InvalidPathDataError


class EntityType(StrEnum):
    SHOT = "shot"
    ASSET = "asset"


class WorkType(StrEnum):
    WORK = "work"
    PUBLISH = "publish"


def _require_slug(value: str, field_name: str) -> str:
    value = value.strip()

    if not value:
        raise InvalidPathDataError(f"{field_name} cannot be empty.")

    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-")
    invalid = set(value) - allowed

    if invalid:
        invalid_chars = "".join(sorted(invalid))
        raise InvalidPathDataError(
            f"{field_name} contains invalid characters: {invalid_chars!r}. "
            "Only letters, numbers, underscores and hyphens are allowed."
        )

    return value


@dataclass(frozen=True)
class Project:
    code: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "code", _require_slug(self.code, "project.code"))


@dataclass(frozen=True)
class Sequence:
    code: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "code", _require_slug(self.code, "sequence.code"))


@dataclass(frozen=True)
class Shot:
    sequence: Sequence
    code: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "code", _require_slug(self.code, "shot.code"))


@dataclass(frozen=True)
class Asset:
    asset_type: str
    name: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "asset_type", _require_slug(self.asset_type, "asset.asset_type"))
        object.__setattr__(self, "name", _require_slug(self.name, "asset.name"))


@dataclass(frozen=True)
class Task:
    name: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", _require_slug(self.name, "task.name"))


@dataclass(frozen=True)
class Version:
    number: int

    def __post_init__(self) -> None:
        if self.number < 1:
            raise InvalidPathDataError("version.number must be greater than or equal to 1.")

    @property
    def label(self) -> str:
        return f"v{self.number:03d}"


@dataclass(frozen=True)
class ParsedPath:
    """
    Result of parsing a library path back into domain data.

    The entity can be either a Shot or an Asset.
    """

    project: Project
    entity: Shot | Asset
    task: Task
    version: Version
    work_type: WorkType
    extension: str
