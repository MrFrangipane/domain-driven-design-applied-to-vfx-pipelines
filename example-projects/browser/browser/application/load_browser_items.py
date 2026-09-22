from pathlib import PurePosixPath

from pipeline_path import PipelinePath, PipelinePathError

from browser.browsing.entities import BrowserItem
from browser.scanning.ports import PathScanner


class LoadBrowserItemsUseCase:
    """
    Application use case for loading browser items from a root path.

    The workflow is:

    1. scan files below a root path;
    2. parse each path with pipeline_path;
    3. skip paths that do not match known templates;
    4. return BrowserItem objects for the paths that were understood.
    """

    def __init__(
        self,
        scanner: PathScanner,
        pipeline_path: PipelinePath,
    ) -> None:
        self._scanner = scanner
        self._pipeline_path = pipeline_path

    def execute(self, root: str | PurePosixPath) -> list[BrowserItem]:
        items: list[BrowserItem] = []

        for path in self._scanner.scan(root):
            try:
                parsed_path = self._pipeline_path.parse_path(path.as_posix())
            except PipelinePathError:
                continue

            items.append(
                BrowserItem(
                    path=path,
                    parsed_path=parsed_path,
                )
            )

        return items
