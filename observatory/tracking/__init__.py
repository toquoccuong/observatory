from concurrent import futures
import grpc

import re
from time import time
from uuid import uuid4
from observatory.protobuf import observatory_pb2, observatory_pb2_grpc
from observatory.tracking.session import TrackingSession


LABEL_PATTERN = '^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,63}(?<!-)$'

server_url = "localhost:5001"


def configure(url='localhost:5001'):
    """
    Configures the observatory environment.
    The following settings can be configured:

     * url - The URL to connect to on the server, by default localhost:5001
    """
    global server_url

    server_url = url


def start_run(name, version, experiment=None):
    """
    Starts a new run for a specific model version
    """

    assert re.match(LABEL_PATTERN, name)
    assert (experiment is None) or re.match(LABEL_PATTERN, experiment)
    assert version > 0

    run_id = str(uuid4())

    channel = grpc.insecure_channel(server_url)
    tracking_stub = observatory_pb2_grpc.TrackingServiceStub(channel)

    return TrackingSession(name, version, run_id, experiment, tracking_stub)
