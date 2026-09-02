from typing import Protocol, Mapping


class PathRenderer(Protocol):
    """
    Port used by the application layer to render a template.

    This keeps the use case independent of any specific rendering engine:
    str.format, Jinja2, custom token resolver, etc.
    """

    def render(self, template: str, values: Mapping[str, object]) -> str:
        raise NotImplementedError
