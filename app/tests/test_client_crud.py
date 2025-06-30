
import pytest
from flask_jwt_extended import JWTManager, create_access_token
from app import create_app, db
from app.models import ClientMetadata, ClientSftpMetadata

@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test-secret",
    })
    JWTManager(app)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            # seed baseline client1
            base = ClientMetadata(client_name="client1", email="client1@example.com")
            db.session.add(base)
            db.session.flush()
            db.session.add(
                ClientSftpMetadata(
                    client_id=base.client_id,
                    sftp_directory="client1",
                    sftp_username="sftp_user1",
                    password="abc123",
                )
            )
            db.session.commit()

        yield client

        with app.app_context():
            db.drop_all()

def auth_header(client):
    with client.application.app_context():
        token = create_access_token(identity="tester")
    return {"Authorization": f"Bearer {token}"}


def test_get_client_metadata(client):
    res = client.get("/client_metadata", headers=auth_header(client))
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list) and data
    assert data[0]["client_name"] == "client1"

def test_add_client_success(client):
    payload = {
        "clientName": "client2",
        "clientEmail": "client2@example.com",
        "sftpUserName": "sftp_user2",
    }
    res = client.post("/client", json=payload, headers=auth_header(client))
    assert res.status_code == 201
    assert "Client added successfully" in res.get_json()["message"]

def test_add_client_missing_field(client):
    payload = {  # missing clientName
        "clientEmail": "missing@example.com",
        "sftpUserName": "sftp_user_missing",
    }
    res = client.post("/client", json=payload, headers=auth_header(client))
    assert res.status_code == 400
    assert "required" in res.get_json()["message"]

def test_add_client_duplicate_name(client):
    payload = {
        "clientName": "client1",  # already exists
        "clientEmail": "dup@example.com",
        "sftpUserName": "dup_sftp",
    }
    res = client.post("/client", json=payload, headers=auth_header(client))
    assert res.status_code == 400
    assert "Client name must be unique" in res.get_json()["message"]

def test_update_client_success(client):
    payload = {
        "client_name": "updated_client1",
        "email": "updated@example.com",
        "permissions": "e",
        "sftp_username": "updated_sftp_user1",
    }
    res = client.put("/client/1", json=payload, headers=auth_header(client))
    assert res.status_code == 200
    assert res.get_json()["client"]["client_name"] == "updated_client1"

def test_update_client_not_found(client):
    res = client.put("/client/999", json={"client_name": "ghost"}, headers=auth_header(client))
    assert res.status_code == 404
    assert "Client not found" in res.get_json()["message"]

def test_delete_client_success(client):
    res = client.delete("/client/1", headers=auth_header(client))
    assert res.status_code == 200
    assert "deleted successfully" in res.get_json()["message"]

def test_delete_client_not_found(client):
    res = client.delete("/client/999", headers=auth_header(client))
    assert res.status_code == 404
    assert "Client not found" in res.get_json()["message"]
