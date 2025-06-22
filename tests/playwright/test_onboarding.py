from playwright.sync_api import sync_playwright
from utils import login

clients = [
    {"client_name": "failTest", "client_email": "", "sftp_user_name": ""},
    {"client_name": "test111", "client_email": "test111@test", "sftp_user_name": "test111@test"},
    {"client_name": "client3", "client_email": "client3@gmail.com", "sftp_user_name": "client3@gmail.com"},
    {"client_name": "client4", "client_email": "client4@gmail.com", "sftp_user_name": "client4@gmail.com"},
    {"client_name": "client5", "client_email": "client5@gmail.com", "sftp_user_name": "client5@gmail.com"},
    {"client_name": "client6", "client_email": "client6@gmail.com", "sftp_user_name": "client6@gmail.com"},
    {"client_name": "client7", "client_email": "client7@gmail.com", "sftp_user_name": "client7@gmail.com"},
    {"client_name": "client8", "client_email": "client8@gmail.com", "sftp_user_name": "client8@gmail.com"},
    {"client_name": "client9", "client_email": "client9@gmail.com", "sftp_user_name": "client9@gmail.com"},
    {"client_name": "client10", "client_email": "client10@gmail.com", "sftp_user_name": "client10@gmail.com"},
    {"client_name": "client11", "client_email": "client11@gmail.com", "sftp_user_name": "client11@gmail.com"},
    {"client_name": "client12", "client_email": "client11@gmail.com", "sftp_user_name": "client11@gmail.com"},
    {"client_name": "client2", "client_email": "client2@gmail.com", "sftp_user_name": "client2@gmail.com"},
    {"client_name": "client1", "client_email": "client1@gmail.com", "sftp_user_name": "client1@gmail.com"},
    {"client_name": "yong", "client_email": "yong@gmail.com", "sftp_user_name": "yong@gmail.com"}
]

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    login(page)

    page.get_by_role("button", name="Onboarding new client").click()
    page.wait_for_load_state('networkidle')

    for client in clients:
        page.fill('#clientName', client["client_name"])
        page.fill('#clientEmail', client["client_email"])
        page.fill('#sftpUserName', client["sftp_user_name"])
        page.get_by_role("button", name="Onboard new client").click()

        success = page.get_by_text("Client added successfully")
        fail = page.get_by_text("Failed to onboard client: Client Name, Client Email, and SFTP Username are required.")

        try:
            success.wait_for(timeout=2000)
            print(f"Client '{client['client_name']}' added successfully.")
        except:
            if fail.is_visible():
                print(f"Failed to add client '{client['client_name']}': Missing fields.")
            else:
                print(f"Unexpected error when adding client '{client['client_name']}'.")

        page.wait_for_timeout(500)  
        page.reload()           

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
