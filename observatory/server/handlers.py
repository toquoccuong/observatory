import time
from os import path, makedirs
from observatory.protobuf import observatory_pb2, observatory_pb2_grpc
import observatory.sink as tracking_sink


class TrackingServiceServicer(observatory_pb2_grpc.TrackingServiceServicer):
    def RecordMetric(self, request, context):
        try:
            tracking_sink.record_metric(
                request.model,
                request.version,
                request.experiment,
                request.run_id,
                request.timestamp,
                request.metric,
                request.value)

            status_code = 200
        except Exception as err:
            print('Failed to record metric.', err)
            status_code = 500

        return observatory_pb2.RecordMetricResponse(status=status_code)

    def RecordSessionStart(self, request, context):
        return observatory_pb2.RecordSessionStartResponse(status=200)

    def RecordSessionCompletion(self, request, context):
        return observatory_pb2.RecordSessionCompletionResponse(status=200)

    def RecordSettings(self, request, context):
        return observatory_pb2.RecordSettingsResponse(status=200)

    def RecordOutput(self, request_iterator, context):
        file_handle = None

        try:
            for chunk in request_iterator:
                if file_handle is None:
                    output_path = path.join(
                        'models', chunk.model, str(chunk.version),
                        chunk.experiment, chunk.run_id)

                    makedirs(output_path, exist_ok=True)

                    output_filename = path.join(output_path, chunk.filename)

                    file_handle = open(output_filename, 'wb')
                
                file_handle.write(chunk.buffer)

            file_handle.close()

            return observatory_pb2.RecordOutputResponse(status=200)
        except Exception as err:
            print(err)
            return observatory_pb2.RecordOutputResponse(status=500)
        finally:
            if not file_handle is None:
                file_handle.close()
