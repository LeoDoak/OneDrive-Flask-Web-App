
'''
This file will test login functionality using pytest.
'''

from server import app


def test_login_valid(monkeypatch):
    '''
    This will test login functionality with valid inputs.
    '''
    def mock_login():
        return True

    monkeypatch.setattr("server.login", mock_login)
    test_client = app.test_client()
    response = test_client.post(
        "/login", data={
            "username": "valid_username", "password": "valid_password"}, follow_redirects=True)
    assert response.headers["Location"] == "http://localhost/homepage"


def test_login_invalid(monkeypatch):
    '''
    This will test login functionality with invalid inputs.
    '''

    def mock_login():
        return False

    monkeypatch.setattr("server.login", mock_login)
    test_client = app.test_client()
    response = test_client.post(
        "/login", data={
            "username": "invalid_username", "password": "invalid_password"}, follow_redirects=True)

    assert b'Incorrect Username or Password!' in response.data
