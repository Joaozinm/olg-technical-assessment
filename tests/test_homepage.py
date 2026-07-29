"""Part 1: basic assertions against the OLG homepage."""

import re

from playwright.sync_api import expect

from pages.olg_home_page import OlgHomePage

# The title carries the current year, so only the stable part is pinned.
TITLE = re.compile(r"^OLG \| Ontario's Online LOTTERY, CASINO & SPORTS \d{4}$")


def test_page_title(olg_home: OlgHomePage) -> None:
    expect(olg_home.page).to_have_title(TITLE)


def test_header_is_visible(olg_home: OlgHomePage) -> None:
    expect(olg_home.header).to_be_visible()


def test_login_button_is_visible(olg_home: OlgHomePage) -> None:
    expect(olg_home.login_button).to_be_visible()
