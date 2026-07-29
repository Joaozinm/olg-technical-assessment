from typing import Self

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage

# The notice renders in well under a second, so a short wait bounds the cost when absent.
NOTICE_TIMEOUT_MS = 2000
# The page reveal lands at about 3.5s.
REVEAL_TIMEOUT_MS = 15000


class OlgHomePage(BasePage):
    """OLG homepage. Resolved against the `base_url` set in pyproject.toml."""

    path = "/en/home.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.header = page.get_by_role("banner")
        self.login_button = page.get_by_role("button", name="Login", exact=True)
        self._privacy_accept = page.get_by_role("button", name="OKAY", exact=True)

    def open(self) -> Self:
        super().open()
        self.wait_until_painted()
        self.dismiss_privacy_notice()
        return self

    def wait_until_painted(self) -> None:
        """Waits out `body { opacity: 0 }`, which Playwright still reports as visible."""
        self.page.wait_for_function(
            "getComputedStyle(document.body).opacity === '1'", timeout=REVEAL_TIMEOUT_MS
        )

    def dismiss_privacy_notice(self) -> None:
        """The privacy notice is not always served, so its absence is not a failure."""
        try:
            self._privacy_accept.click(timeout=NOTICE_TIMEOUT_MS)
        except PlaywrightTimeoutError:
            pass
