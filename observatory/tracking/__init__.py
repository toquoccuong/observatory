from concurrent import futures
import grpc

import re
from time import time
from uuid import uuid4
from observatory.protobuf import observatory_pb2, observatory_pb2_grpc
from observatory.tracking.session import TrackingSession


LABEL_PATTERN = '^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,63}(?<!-)$'

server_url = "localhost:5001"


def configure(url):
    """
    Configures the observatory environment.
    The following settings can be configured:

    Parameters
    ----------
    url : string
        The URL to connect to for tracking session information
    """
    global server_url

    server_url = url


def start_run(name, version, experiment='default'):
    """
    Starts a new run for a specific model version
    """

    if not re.match(LABEL_PATTERN, name):
        raise AssertionError('name is invalid. It can contain ' +
                             'lower-case alpha-numeric characters and dashes only.')

    if experiment is None:
        experiment = 'default'

    if experiment != 'default' and not re.match(LABEL_PATTERN, name):
        raise AssertionError('experiment is invalid. It can contain ' +
                             'lower-case alpha-numeric characters and dashes only.')

    if version <= 0:
        raise AssertionError('version must be greater than zero')

    run_id = str(uuid4())

    channel = grpc.insecure_channel(server_url)
    tracking_stub = observatory_pb2_grpc.TrackingServiceStub(channel)

    return TrackingSession(name, version, experiment, run_id, tracking_stub)
