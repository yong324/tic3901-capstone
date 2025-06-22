# tests/playwright/utils.py
def login(page, username="yong", password="password123"):
    """Reusable login function for all tests"""
    page.goto("http://localhost:8080/")
    page.get_by_placeholder("Username").fill(username)
    page.get_by_placeholder("Password").fill(password)
    page.get_by_role("button", name="Login").click()
    page.wait_for_load_state('networkidle')
