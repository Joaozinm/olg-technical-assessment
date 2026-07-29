"""Part 2: restaurant search on Google Maps."""

from playwright.sync_api import expect

from pages.google_maps_home_page import GoogleMapsHomePage

# Maps renders results in about 6s. Scoped here so Part 1 keeps fast failure feedback.
RESULTS_TIMEOUT_MS = 15000


def test_search_returns_at_least_one_restaurant(maps_home: GoogleMapsHomePage) -> None:
    first_result = maps_home.search_for("Restaurants").items.first
    # Both checks make one claim: a result is rendered and actually on screen.
    # to_be_visible alone ignores the viewport, so an off-screen result would pass.
    expect(first_result).to_be_visible(timeout=RESULTS_TIMEOUT_MS)
    expect(first_result).to_be_in_viewport()
