import re
from playwright.sync_api import expect
from utils import login

def test_login_success(page):
    login(page, username="yong", password="password123")
    expect(page).to_have_url(re.compile(r"/landingpage$"))

def test_login_invalid_credentials(page):
    login(page, username="yong", password="wrongpassword")
    expect(page).to_have_url(re.compile(r"/"))
    expect(page.get_by_text(re.compile(r"Invalid username or password", re.I))).to_be_visible()
