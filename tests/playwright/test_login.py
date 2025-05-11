from playwright.sync_api import sync_playwright
from utils import login

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    
    login(page)

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
