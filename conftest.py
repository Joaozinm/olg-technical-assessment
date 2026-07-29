import pytest
from playwright.sync_api import Page

from pages.olg_home_page import OlgHomePage


@pytest.fixture
def olg_home(page: Page) -> OlgHomePage:
    return OlgHomePage(page).open()
