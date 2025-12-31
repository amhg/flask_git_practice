import pytest
from main import app as flask_app
from unittest.mock import patch, MagicMock
from flask import url_for

@pytest.fixture(autouse=True)
def client():
    with flask_app.test_client() as client:
        yield client


def test_add_login_success(client):
    # Patch LoginRepository and return True on insert
    with patch('modules.repository.login.LoginRepository') as mock_repo_class:
        mock_repo = MagicMock()
        mock_repo.insert.return_value = True
        mock_repo_class.return_value = mock_repo

        # Prepare form data (simulate browser POST)
        data = {
            'username': 'testuser',
            'password': 'testpass',
            'user_type': '0',
            'csrf_token': 'dummy_csrf_token'  # required unless CSRF disabled
        }

        # Disable CSRF for testing unless explicitly testing it
        with client.session_transaction() as sess:
            sess['_csrf_token'] = data['csrf_token']

        response = client.post('/login/add', data=data, follow_redirects=True)

        assert response.status_code == 200
        assert b"New User added" in response.data


