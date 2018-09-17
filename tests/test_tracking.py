import json
import requests
from observatory.tracking import TrackingSession, TrackingClient

class MockResponse:
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content

    def json(self):
        return json.loads(self.content)


def test_record_metrics(mocker):
    mock_response = mocker.Mock(requests.Response, status_code=201)

    method_attrs = {
        'record_metric.return_value': mock_response,
        'record_session_start.return_value': mock_response,
        'record_session_end.return_value': mock_response
    }

    client = mocker.Mock(TrackingClient, **method_attrs)

    with TrackingSession('test',1,'test','test',client) as session:
        session.record_metric('test', 1.0)        

    client.record_session_start.assert_called()
    client.record_metric.assert_called()
    client.record_session_end.assert_called()
    
def test_record_output(mocker):
    mock_response = mocker.Mock(requests.Response, status_code=201)

    method_attrs = {
        'record_output.return_value': mock_response,
        'record_session_start.return_value': mock_response,
        'record_session_end.return_value': mock_response
    }

    client = mocker.Mock(TrackingClient, **method_attrs)

    with open('test.txt','w') as test_file:
        test_file.write('test')

    with TrackingSession('test', 1, 'test', 'test', client) as session:
        session.record_output('test.txt', 'test.txt')

    client.record_session_start.assert_called()
    client.record_output.assert_called()
    client.record_session_end.assert_called()
