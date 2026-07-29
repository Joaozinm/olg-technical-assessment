"""Part 1 on a mobile viewport: the same visible elements, reached differently.

The page title is not repeated here. It comes from the same document regardless of
viewport, so asserting it again would re-check an identical string.
"""

from playwright.sync_api import expect

from pages.olg_home_page import OlgHomePage


def test_header_is_visible_on_mobile(olg_home_mobile: OlgHomePage) -> None:
    expect(olg_home_mobile.header).to_be_visible()


def test_login_button_is_visible_on_mobile(olg_home_mobile: OlgHomePage) -> None:
    olg_home_mobile.open_navigation_menu()
    expect(olg_home_mobile.login_button).to_be_visible()
