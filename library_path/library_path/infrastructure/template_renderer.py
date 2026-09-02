from string import Formatter
from typing import Mapping

from library_path.application.builder.path_renderer import PathRenderer
from library_path.domain.exceptions import InvalidPathDataError


class FormatStringPathRenderer(PathRenderer):
    """
    Adapter using Python's built-in str.format syntax.

    Example template:

        /show/{project}/shots/{shot}/{task}/{version}/{name}_{version}.{extension}
    """

    def render(self, template: str, values: Mapping[str, object]) -> str:
        missing_keys = self._find_missing_keys(template, values)

        if missing_keys:
            missing = ", ".join(sorted(missing_keys))
            raise InvalidPathDataError(f"Cannot render path template. Missing values: {missing}.")

        return template.format(**values)

    def _find_missing_keys(self, template: str, values: Mapping[str, object]) -> set[str]:
        formatter = Formatter()
        required_keys: set[str] = set()

        for _, field_name, _, _ in formatter.parse(template):
            if field_name:
                required_keys.add(field_name)

        return required_keys - set(values)
