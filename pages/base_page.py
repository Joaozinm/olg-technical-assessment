from typing import Self

from playwright.sync_api import Page


class BasePage:
    """Shared page setup. Subclasses with an entry point set `path`.

    Public locators are what tests assert on; private ones serve the page's own actions.
    """

    path: str  # No default, so a page with no entry point fails loudly on open().

    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self) -> Self:
        # `load` waits on every subresource, which third party trackers can stall past
        # 30s. Pages needing more than a parsed DOM wait for their own ready signal.
        self.page.goto(self.path, wait_until="domcontentloaded")
        return self
