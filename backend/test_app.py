
import pytest
from app import create_app, db, UserCredentials, ClientMetadata, ClientSftpMetadata

@pytest.fixture
def test_client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            user = UserCredentials(username='testuser', password='testpass', role='admin')
            client_metadata = ClientMetadata(client_name='client1', email='client1@example.com')
            sftp = ClientSftpMetadata(client_id=1, sftp_directory='client1', sftp_username='sftp_user1', password='client1_abcd')
            db.session.add_all([user, client_metadata, sftp])
            db.session.commit()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

def test_login_success(test_client):
    response = test_client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Login successful'

def test_login_failure(test_client):
    response = test_client.post('/login', json={'username': 'wrong', 'password': 'bad'})
    assert response.status_code == 401
    assert 'Invalid' in response.get_json()['message']

def test_get_client_metadata(test_client):
    response = test_client.get('/client_metadata')
    data = response.get_json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert data[0]['client_name'] == 'client1'

def test_add_client_success(test_client):
    response = test_client.post('/client', json={
        'clientName': 'client2',
        'clientEmail': 'client2@example.com',
        'sftpUserName': 'sftp_user2'
    })
    assert response.status_code == 201
    assert 'Client added successfully' in response.get_json()['message']

def test_add_client_duplicate_name(test_client):
    response = test_client.post('/client', json={
        'clientName': 'client1',
        'clientEmail': 'client1@example.com',
        'sftpUserName': 'sftp_user1'
    })
    assert response.status_code == 400
    assert 'Client name must be unique' in response.get_json()['message']

def test_add_client_missing_field(test_client):
    response = test_client.post('/client', json={
        'clientEmail': 'missing@example.com',
        'sftpUserName': 'sftp_user_missing'
    })
    assert response.status_code == 400
    assert 'required' in response.get_json()['message']

def test_update_client_success(test_client):
    response = test_client.put('/client/1', json={
        'client_name': 'updated_client1',
        'email': 'updated@example.com',
        'permissions': 'write',
        'sftp_username': 'updated_sftp_user1'
    })
    assert response.status_code == 200
    assert response.get_json()['client']['client_name'] == 'updated_client1'

def test_update_client_not_found(test_client):
    response = test_client.put('/client/999', json={
        'client_name': 'ghost_client'
    })
    assert response.status_code == 404
    assert 'Client not found' in response.get_json()['message']

def test_delete_client_success(test_client):
    response = test_client.delete('/client/1')
    assert response.status_code == 200
    assert 'deleted successfully' in response.get_json()['message']

def test_delete_client_not_found(test_client):
    response = test_client.delete('/client/999')
    assert response.status_code == 404
    assert 'Client not found' in response.get_json()['message']
