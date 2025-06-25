import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # swap to True in CI
        page = browser.new_page()
        yield page
        browser.close()
