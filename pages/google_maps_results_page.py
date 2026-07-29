from playwright.sync_api import Page

from pages.base_page import BasePage


class GoogleMapsResultsPage(BasePage):
    """Google Maps results. Reached through GoogleMapsHomePage.search_for()."""

    def __init__(self, page: Page, term: str) -> None:
        super().__init__(page)
        # The feed name binds items to the term searched, so a stale result set cannot pass.
        self.items = page.get_by_role("feed", name=f"Results for {term}").get_by_role("article")
