'''
Tests for groups creation
'''


from server import app


def test_create_group_valid(monkeypatch):
    '''
    User story #2. Tests creating a valid group.
    If successful, response should redirect to the groups page.
    '''
    def mock_create_group():
        return True

    monkeypatch.setattr("server.create_group", mock_create_group)
    test_client = app.test_client()
    response = test_client.post(
        "/create_group", data={
            "group_name": "Test Group"
        }, follow_redirects=True)
    assert response.headers["Location"] == "http://localhost/group"


def test_create_group_invalid(monkeypatch):
    '''
    User story #2. Tests creating an invalid group, such as missing group name.
    Asserts that the response contains an error message.
    '''
    def mock_create_group():
        return False

    monkeypatch.setattr("server.create_group", mock_create_group)
    test_client = app.test_client()
    response = test_client.post(
        "/create_group", data={
            "group_name": "",  # Empty group name
        }, follow_redirects=True)
    assert b'Error creating group' in response.data
