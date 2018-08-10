from time import time
from observatory.protobuf import observatory_pb2, observatory_pb2_grpc


class TrackingSession:
    """
    Keeps all tracking information for a single training session together in one neat package.
    You can use this class to record various things about your model.
    """

    def __init__(self, name, version, experiment, run_id, tracking_stub):
        """
        Initializes the tracking session with the necessary tracking information
        and a pre-initialized tracking client for recording the actual metrics.
        """
        self.name = name
        self.version = version
        self.run_id = run_id
        self.tracking_stub = tracking_stub
        self.experiment = experiment

    def record_metric(self, name, value):
        """
        Records a metric value on the server
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

    def __enter__(self):
        timestamp = int(time())

        request = observatory_pb2.RecordSessionStartRequest(
            model=self.name,
            version=self.version,
            experiment=self.experiment,
            run_id = self.run_id,
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
            run_id = self.run_id,
            timestamp=timestamp,
            status=session_status
        )

        response = self.tracking_stub.RecordSessionCompletion(request)

        if response.status != 200:
            raise RuntimeError('Failed to record session completion')

        return exc_type is None