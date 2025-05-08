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
        'permissions': 'e',
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
