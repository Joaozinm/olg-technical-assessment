# olg-technical-assessment

UI automation assessment for the QA Automation Engineer position at OLG.

- **Part 1: Basic Assertions** on [olg.ca](https://www.olg.ca/en/home.html), desktop and mobile
- **Part 2: Search Scenario** searching "Restaurants" on [Google Maps](https://www.google.com/maps)

## Install and run

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run playwright install chromium
uv run pytest
```

| Command | Runs |
| --- | --- |
| `uv run pytest` | The 6 tests on Chromium |
| `uv run pytest --headed` | The same, with a visible browser |
| `uv run pytest -k mobile` | The 2 mobile tests only |
| `uv run playwright install firefox webkit` | Once, before the line below |
| `uv run pytest --browser firefox --browser webkit` | The suite on the other two engines |

The mobile tests carry their own emulated device, so they need no flag. A global `--device` would
push the desktop tests onto a phone, where they are expected to fail. Failures leave a screenshot,
a video and a trace in `artifacts/`. The trace carries a DOM snapshot per action, plus network and
console, and opens with:

```bash
uv run playwright show-trace artifacts/<test-name>/trace.zip
```

## Tools and why

| Tool | Why |
| --- | --- |
| Playwright | Auto-waiting removes explicit sleeps, the main source of UI flakiness. Cross-browser out of the box. |
| Python | The sync Playwright API keeps tests linear and readable. |
| pytest | Fixtures give setup and teardown, with a browser context isolated per test. |
| pytest-playwright | Supplies the `page` fixture, the `--browser` and `--headed` flags, and failure artifacts. |
| uv | Reproducible installs from a committed lockfile. |
| ruff | Format and lint in one tool. |

## Test structure

```
├── conftest.py                      # fixtures, one per site plus a mobile variant
├── pyproject.toml                   # dependencies, pytest and ruff configuration
├── pages/
│   ├── base_page.py                 # shared navigation
│   ├── olg_home_page.py             # Part 1, desktop and mobile
│   ├── google_maps_home_page.py     # Part 2, search entry point
│   └── google_maps_results_page.py  # Part 2, result items
└── tests/
    ├── test_homepage.py             # title, header, login button
    ├── test_homepage_mobile.py      # header and login on an emulated iPhone 13
    └── test_restaurant_search.py    # at least one restaurant result, on screen
```

Page Object Model: pages own locators and actions, tests own assertions, and navigation is
modelled by return type, so `search_for()` hands back a `GoogleMapsResultsPage`. Public locators
are what tests assert on, private ones serve the page's own actions. The mobile tests reuse
`OlgHomePage` with one extra action, `open_navigation_menu()`, because only the route to the
element changes.

Locators are ARIA roles and accessible names rather than CSS or XPath, so they survive styling
changes and fail when an element stops being accessible. Assertions use `expect`, which retries
until its timeout. One behaviour per test.

## Assumptions and limitations

- Live production sites, so the suite depends on availability, content changes and bot protection.
- Maps results follow the client IP, so the test asserts that a result exists, never a business
  name. `hl=en` pins the UI language the accessible-name locators depend on.
- Mobile covers Part 1 only. Maps mobile web has no search input: the affordance is a
  `div[role=button]` that redirects to an app landing page, and the `feed` landmark is absent.
  Results are reachable only by deep link, which would assert without performing a search.
- The OLG privacy notice is dismissed when present and tolerated when absent.
- Chromium is the default. Firefox and WebKit pass, but are not installed by `uv sync`.
- No authentication. Everything asserted is public to a signed-out visitor.

## What I would improve with more time

- CI on GitHub Actions, running the browser matrix on every push and publishing failure artifacts.
- Pin the Maps location with a geolocation override so results are deterministic.
- Accessibility checks with axe-core, and visual regression on the header.
- Move expected copy to a data file so a content change is a one-line update.
