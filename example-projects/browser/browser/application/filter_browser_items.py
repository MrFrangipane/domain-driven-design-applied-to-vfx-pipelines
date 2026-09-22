from browser.browsing.entities import BrowserFilter, BrowserItem


class FilterBrowserItemsUseCase:
    """
    Application use case for applying browser filters.

    This stays independent of any UI. A Qt controller, CLI, test, or another
    tool can call it with plain BrowserItem objects.
    """

    def execute(
        self,
        items: list[BrowserItem],
        browser_filter: BrowserFilter,
    ) -> list[BrowserItem]:
        return [
            item
            for item in items
            if browser_filter.matches(item)
        ]
