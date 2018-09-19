import requests
from observatory.serving import download_model

def test_download_model(mocker):
    def content_iterator(size):
        yield b''

    mock_response = mocker.Mock(requests.Response, status_code=200, autospec=True, iter_content=content_iterator)

    requests_mock = mocker.patch('observatory.serving.requests')
    requests_mock.get.return_value = mock_response
    
    mock_archive = mocker.patch('observatory.serving.archive')
    
    download_model(model='test', version=1, run_id='test')

    mock_archive.extract.assert_called()
