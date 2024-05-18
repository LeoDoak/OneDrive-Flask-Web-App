
'''
This file will test upload functionality using pytest.
'''
from server import app


def test_upload_valid(monkeypatch):
    '''
    User story #1. Tests a valid file png upload.
    If successful, response should take the user back to groups page.
    '''
    def mock_upload():
        return True

    monkeypatch.setattr("server.upload_page_action", mock_upload)
    test_client = app.test_client()
    response = test_client.post(
        "/upload_page_action", data={
            "file": 'static/filetest/mcd.png'}, follow_redirects=True)
    assert response.headers["Location"] == "http://localhost/file_groups"


def test_upload_invalid(monkeypatch):
    '''
    # User story #1. Tests an invalid upload, such as a String.
    Asserts that the response is an Invalid File.
    '''
    def mock_upload():
        return True

    monkeypatch.setattr("server.upload_page_action", mock_upload)
    test_client = app.test_client()
    response = test_client.post(
        "/upload_page_action", data={
            "file": "teststring"}, follow_redirects=True)

    assert b'Invalid File' in response.data
