import re

def _register_user(client, username="testuser", password="testpass"):
    """
    Register a user through the public /register endpoint.
    If the user already exists, 409 is acceptable for re-runs.
    """
    resp = client.post(
        "/register",
        json={"username": username, "password": password},
    )
    assert resp.status_code in (201, 409)  # 409 = "Username already exists"


def test_login_success(test_client):
    _register_user(test_client)  # ensure account exists

    res = test_client.post(
        "/login",
        json={"username": "testuser", "password": "testpass"},
    )
    assert res.status_code == 200

    data = res.get_json()
    assert data["message"] == "Login successful"
    assert {"role", "user_id"} <= data.keys()  # both keys present

    # JWT cookies must be set (access, refresh, CSRF)
    cookies = "; ".join(res.headers.getlist("Set-Cookie"))
    assert re.search(r"access_token_cookie=.*;",  cookies)
    assert re.search(r"refresh_token_cookie=.*;", cookies)
    assert re.search(r"csrf_access_token=.*;",    cookies)


def test_login_failure(test_client):
    res = test_client.post(
        "/login",
        json={"username": "nonexistentuser", "password": "wrongpass"},
    )

    assert res.status_code == 401
    assert "Invalid" in res.get_json()["message"]
