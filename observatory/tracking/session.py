import json
from time import time
from observatory.protobuf import observatory_pb2, observatory_pb2_grpc

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
