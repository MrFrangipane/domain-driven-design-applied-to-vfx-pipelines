import sys

from pipeline_path import PipelinePath
from pipeline_path.domain.entities import WorkType

from browser.application import FilterBrowserItemsUseCase, LoadBrowserItemsUseCase
from browser.browsing import BrowserFilter
from browser.scanning import FilesystemPathScanner

loader = LoadBrowserItemsUseCase(
    scanner=FilesystemPathScanner(),
    pipeline_path=PipelinePath.default(),
)

items = loader.execute(sys.argv[1])

filtered_items = FilterBrowserItemsUseCase().execute(
    items=items,
    browser_filter=BrowserFilter(
        project_code="an-awesome-show",
        work_type=WorkType.WORK,
        search_text="animation",
    ),
)

for item in filtered_items:
    print(item.path.as_posix())
