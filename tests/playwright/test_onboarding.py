import pytest
import re
from datetime import datetime
import secrets                       
from playwright.sync_api import expect
from utils import login

def make_unique_base(prefix: str = "e2eTest") -> str:
    """Return something like  e2eTest_20250625143017_4821"""
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")      # yyyymmddhhmmss
    rand  = secrets.randbelow(10_000)                    # 0-9999
    return f"{prefix}_{stamp}_{rand:04d}"

unique = make_unique_base()                              


clients = [
    # name                  email                     sftp                  should      err
    ("noEmailTest",         "",                       "",                   False,      "Failed to onboard client"),
    ("duplicatedClient",    "duplicate@gmail.com",    "duplicate@gmail.com",False,      "Client name must be unique"),
    (unique,                f"{unique}@gmail.com",    f"{unique}@gmail.com",True,       None),
]


@pytest.mark.parametrize(
    "name,email,sftp,should_succeed,error_snippet",
    clients,
    ids=[row[0] for row in clients],
)
def test_onboard_client(page, name, email, sftp, should_succeed, error_snippet):
    login(page)
    page.get_by_role("button", name="Onboarding new client").click()
    #page.wait_for_load_state('networkidle')
    page.fill("#clientName", name)
    page.fill("#clientEmail", email)
    page.fill("#sftpUserName", sftp)
    page.get_by_role("button", name="Onboard new client").click()

    if should_succeed:
        expect(page.get_by_text("Client added successfully")).to_be_visible()
    else:
        expect(page.get_by_text(re.compile(error_snippet))).to_be_visible()
