from concurrent import futures
import grpc

import re
from uuid import uuid4
from observatory.protobuf import observatory_pb2, observatory_pb2_grpc
from observatory.tracking.session import TrackingSession
from observatory import settings
from observatory.constants import LABEL_PATTERN


def start_run(model, version, experiment='default'):
    """
    Starts a new run for a specific model version.

    You can use this function start start recording data related to a single experiment run.
    The use of experiments is optional, you can leave this parameter out. See the example below for basic usage.

    >>> with observatory.start_run('my_model', 1, experiment='my_experiment') as run:
    >>>     # Record metrics, outputs and settings

    A new run is created on the server at the start of the scope.
    It is automatically finalized at the end of the scope.

    Note that when an exception occurs within the scope of a run,
    the run is automatically marked as failed.

    Each time you invoke `start_run` a new run is created with a newly generated UUID.
    This ensures that no runs overlap eachother.

    **Please note** it is not possible to resume a run that you started earlier.

    Parameters
    ----------
    model : string
        The name of the model
    version : int
        The version number of the model
    experiment : string, optional
        The experiment you're working on
    """

    if not re.match(LABEL_PATTERN, model):
        raise AssertionError('name is invalid. It can contain ' +
                             'lower-case alpha-numeric characters and dashes only.')

    if experiment is None:
        experiment = 'default'

    if experiment != 'default' and not re.match(LABEL_PATTERN, model):
        raise AssertionError('experiment is invalid. It can contain ' +
                             'lower-case alpha-numeric characters and dashes only.')

    if version <= 0:
        raise AssertionError('version must be greater than zero')

    run_id = str(uuid4())

    channel = grpc.insecure_channel(settings.server_url)
    tracking_stub = observatory_pb2_grpc.TrackingServiceStub(channel)

    return TrackingSession(model, version, experiment, run_id, tracking_stub)
