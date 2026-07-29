from collections.abc import Iterator

import pytest
from playwright.sync_api import Browser, Page, Playwright

from pages.google_maps_home_page import GoogleMapsHomePage
from pages.olg_home_page import OlgHomePage

# Emulates viewport, user agent, touch and device scale, not just a narrow window.
MOBILE_DEVICE = "iPhone 13"


@pytest.fixture
def olg_home(page: Page) -> OlgHomePage:
    return OlgHomePage(page).open()


@pytest.fixture
def olg_home_mobile(
    browser: Browser, playwright: Playwright, browser_context_args: dict
) -> Iterator[OlgHomePage]:
    context = browser.new_context(**{**browser_context_args, **playwright.devices[MOBILE_DEVICE]})
    try:
        yield OlgHomePage(context.new_page()).open()
    finally:
        # Without this, a failure during open() would leak the context.
        context.close()


@pytest.fixture
def maps_home(page: Page) -> GoogleMapsHomePage:
    return GoogleMapsHomePage(page).open()
