from unittest.mock import patch

def test_add_client_internal_error(test_client):
    with patch("app.routes.generate_password", side_effect=Exception("Simulated password generation failure")):
        response = test_client.post('/client', json={
            'clientName': 'fail_client',
            'clientEmail': 'fail@example.com',
            'sftpUserName': 'fail_user'
        })
        assert response.status_code == 500
        assert "Failed to add client" in response.get_json()['message']

def test_update_client_internal_error(test_client):
    with patch("app.routes.format_client", side_effect=Exception("Simulated format failure")):
        response = test_client.put('/client/1', json={
            'client_name': 'error_client',
            'email': 'error@example.com',
            'permissions': 'e',
            'sftp_username': 'error_user'
        })
        assert response.status_code == 500
        assert "Failed to update client" in response.get_json()['message']

def test_delete_client_internal_error(test_client):
    with patch("app.routes.db.session.commit", side_effect=Exception("Simulated delete failure")):
        response = test_client.delete('/client/1')
        assert response.status_code == 500
        assert "Failed to delete client" in response.get_json()['message']
