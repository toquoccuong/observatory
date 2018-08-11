import time
from observatory.protobuf import observatory_pb2, observatory_pb2_grpc


class TrackingServiceServicer(observatory_pb2_grpc.TrackingServiceServicer):
    def RecordMetric(self, request, context):
        return observatory_pb2.RecordMetricResponse(status=200)

    def RecordSessionStart(self, request, context):
        return observatory_pb2.RecordSessionStartResponse(status=200)

    def RecordSessionCompletion(self, request, context):
        return observatory_pb2.RecordSessionCompletionResponse(status=200)

    def RecordSettings(self, request, context):
        return observatory_pb2.RecordSettingsResponse(status=200)