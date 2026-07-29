from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.google_maps_results_page import GoogleMapsResultsPage


class GoogleMapsHomePage(BasePage):
    """Google Maps. `hl=en` pins the UI language, which otherwise follows the client IP."""

    path = "https://www.google.com/maps?hl=en"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._search_box = page.get_by_role("combobox", name="Search Google Maps")
        self._search_button = page.get_by_role("button", name="Search", exact=True)

    def search_for(self, term: str) -> GoogleMapsResultsPage:
        self._search_box.fill(term)
        self._search_button.click()
        return GoogleMapsResultsPage(self.page, term)
