from unittest.mock import patch
from flask_jwt_extended import create_access_token

def auth_header(test_client):
    with test_client.application.app_context():
        token = create_access_token(identity="tester")
    return {"Authorization": f"Bearer {token}"}


def test_add_client_internal_error(test_client):
    with patch("app.routes.generate_password", side_effect=Exception("Simulated password generation failure")):
        res = test_client.post(
            "/client",
            json={
                "clientName": "fail_client",
                "clientEmail": "fail@example.com",
                "sftpUserName": "fail_user"
            },
            headers=auth_header(test_client)
        )
        assert res.status_code == 500
        assert "Failed to add client" in res.get_json()["message"]


def test_update_client_internal_error(test_client):
    with patch("app.routes.format_client", side_effect=Exception("Simulated format failure")):
        res = test_client.put(
            "/client/1",
            json={
                "client_name": "error_client",
                "email": "error@example.com",
                "permissions": "e",
                "sftp_username": "error_user"
            },
            headers=auth_header(test_client)
        )
        assert res.status_code == 500
        assert "Failed to update client" in res.get_json()["message"]


def test_delete_client_internal_error(test_client):
    with patch("app.routes.db.session.commit", side_effect=Exception("Simulated delete failure")):
        res = test_client.delete("/client/1", headers=auth_header(test_client))
        assert res.status_code == 500
        assert "Failed to delete client" in res.get_json()["message"]
