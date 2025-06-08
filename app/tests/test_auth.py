def test_login_success(test_client):
    response = test_client.post('/login', json={
        'username': 'testuser',
        'password': 'testpass' 
    })

    assert response.status_code == 200
    assert response.get_json()['message'] == 'Login successful'
    assert 'role' in response.get_json()
    assert 'user_id' in response.get_json()


def test_login_failure(test_client):
    response = test_client.post('/login', json={
        'username': 'nonexistentuser',
        'password': 'wrongpass'
    })

    assert response.status_code == 401
    assert 'Invalid' in response.get_json()['message']
