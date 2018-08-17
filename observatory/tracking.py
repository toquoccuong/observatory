from concurrent import futures
import grpc

import json
import re
from uuid import uuid4
from time import time
from observatory.protobuf import observatory_pb2, observatory_pb2_grpc
from observatory import settings
from observatory.constants import LABEL_PATTERN

CHUNK_SIZE = 1024 * 1024


class TrackingSession:
    """
    The tracking session is used to track data related to a single training run.

    When you invoke :func:`start_run <observatory.start_run>` this class is instantiated for you
    with the correct settings to start tracking data.

    Any server connection used by the tracking logic is automatically opened and closed for you.
    """

    def __init__(self, name, version, experiment, run_id, tracking_stub):
        """
        Initializes the tracking session with the necessary tracking information
        and a pre-initialized tracking client for recording the actual metrics.

        Parameters
        ----------
        name : string
            Name of the model
        version : int
            Version number of the model
        experiment : string
            Name of the experiment
        run_id : string
            ID of the run
        tracking_stub : object
            Instance of the tracking service stub
        """
        self.name = name
        self.version = version
        self.run_id = run_id
        self.tracking_stub = tracking_stub
        self.experiment = experiment

    def record_metric(self, name, value):
        """
        Records a metric value on the server

        Parameters
        ----------
        name : string
            The name of the metric to record
        value : float
            The value of the metric to records
        """
        timestamp = int(time())

        request = observatory_pb2.RecordMetricRequest(
            model=self.name,
            version=self.version,
            experiment=self.experiment,
            run_id=self.run_id,
            timestamp=timestamp,
            metric=name,
            value=value)

        response = self.tracking_stub.RecordMetric(request)

        if response.status != 200:
            raise RuntimeError('Failed to record metric')

    def record_settings(self, **settings):
        """
        Records settings used for the run

        Parameters
        ----------
        settings : object
            A dictionary containing all settings used for the run.
            This can be passed in as `key=value` pairs.
        """
        request = observatory_pb2.RecordSettingsRequest(
            model=self.name,
            version=self.version,
            experiment=self.experiment,
            run_id=self.run_id,
            data=json.dumps(settings))

        response = self.tracking_stub.RecordSettings(request)

        if response.status != 200:
            raise RuntimeError('Failed to record settings')

    def record_output(self, input_file, filename):
        """
        Records an output for the current run.

        Parameters
        ----------
        input_file : object
            Filename or handle to input file
        filename : string
            Name of the file as it should be stored on the server
        """

        def chunker(model, version, experiment, run_id, out_file, file):
            if type(file) == str:
                file_handle = open(file, 'rb')
            else:
                file_handle = input_file

            while True:
                chunk_data = file_handle.read(CHUNK_SIZE)

                if len(chunk_data) == 0:
                    return

                chunk = observatory_pb2.Chunk(
                    model=model,
                    version=version,
                    experiment=experiment,
                    run_id=run_id,
                    filename=out_file,
                    buffer=chunk_data)

                yield chunk

        response = self.tracking_stub.RecordOutput(
            chunker(self.name, self.version, self.experiment, self.run_id, filename, input_file))

        if response.status != 200:
            raise RuntimeError('Failed to record output')

    def __enter__(self):
        timestamp = int(time())

        request = observatory_pb2.RecordSessionStartRequest(
            model=self.name,
            version=self.version,
            experiment=self.experiment,
            run_id=self.run_id,
            timestamp=timestamp
        )

        response = self.tracking_stub.RecordSessionStart(request)

        if response.status != 200:
            raise RuntimeError('Failed to record session start')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            session_status = 'COMPLETED'
        else:
            session_status = 'FAILED'

        timestamp = int(time())

        request = observatory_pb2.RecordSessionCompletionRequest(
            model=self.name,
            version=self.version,
            experiment=self.experiment,
            run_id=self.run_id,
            timestamp=timestamp,
            status=session_status
        )

        response = self.tracking_stub.RecordSessionCompletion(request)

        if response.status != 200:
            raise RuntimeError('Failed to record session completion')

        return exc_type is None


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
