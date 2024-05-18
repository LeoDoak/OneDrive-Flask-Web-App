
'''
This file will test upload functionality using pytest.
'''
from unittest.mock import Mock, patch
import json
import sys
from server import app
sys.path.insert(1, '')


def test_search_files_valid(monkeypatch):
    '''
    User story #4. Tests searching for files with valid search criteria.
    If successful, response should contain the files that match the criteria.
    '''
    def mock_requests_get():
        # Mock response data for the Graph API call
        data = {
            "value": [
                {"id": "file_id_1", "name": "Test Document.docx"},
                {"id": "file_id_2", "name": "Test Presentation.pptx"}
            ]
        }
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.text = json.dumps(data)
        return response_mock
    # Replace the 'requests.get' call with the mock
    monkeypatch.setattr('requests.get', mock_requests_get)
    # Mock File class used within the searchfiles function
    with patch('server.File') as mock_file_class:
        mock_file_instance = mock_file_class.return_value
        mock_file_instance.set_file_icon.return_value = None
        mock_file_instance.set_filetype.return_value = None
        mock_file_instance.fileicon = '/static/icon/docx_icon.png'
        mock_file_instance.title = 'Test Document'
        # Use test client to send a POST request to the search endpoint
        test_client = app.test_client()
        response = test_client.post('/searchfiles', data={'Search': 'Test'})
        # Assertions to check if the response contains the expected files
        assert response.status_code == 200
        assert b'Test Document' in response.data
        assert b'Test Presentation' in response.data


def test_search_files_invalid(monkeypatch):
    '''
    User story #4. Tests searching for files with invalid search criteria or when an error occurs.
    The response should handle the error gracefully.
    '''
    def mock_requests_get():
        # Mock an error in the Graph API call
        response_mock = Mock()
        response_mock.status_code = 500
        response_mock.text = json.dumps({"error": {"code": "internalServerError"}})
        return response_mock
    # Replace the 'requests.get' call with the mock
    monkeypatch.setattr('requests.get', mock_requests_get)
    # Use test client to send a POST request to the search endpoint
    test_client = app.test_client()
    response = test_client.post('/searchfiles', data={'Search': 'Nonexistent'})
    # Assertions to check for error handling
    assert response.status_code == 500 or 'Error' in response.data
