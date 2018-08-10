import time
from observatory.protobuf import observatory_pb2, observatory_pb2_grpc


class TrackingServiceServicer(observatory_pb2_grpc.TrackingServiceServicer):
    """
    Implements the logic to handle incoming tracking requests.
    Every method here reflects the same method on the TrackingSession class on the client.
    """
    
    def RecordMetric(self, request, context):
        """
        Handles recording of metrics on the server.

        When the client uses record_metric, this method gets invoked on the server.
        The client will send the following data:

         - Name of the model
         - Version of the model
         - The name of the experiment
         - The ID of the run
         - The name of the metric
         - The value for the metric

        Parameters
        ----------
        request : object
            The incoming request data
        context : object
            The context information for the request

        Returns
        -------
        observatory.protobuf.observatory_pb2.RecordMetricResponse
            This method will return a response with a status code.
            The following status codes are supported:

            - 200: OK
            - 400: Bad input
            - 500: Internal error
        """
        response = observatory_pb2.RecordMetricResponse()
        response.status = 200

        print('Recorded metric')
        print(request)

        return response

    def RecordSessionStart(self, request, context):
        """
        This method records the start of a training session.
        For every training session the following information is recorded:

         - Name of the model
         - Version of the model
         - The name of the experiment
         - The ID of the run
         - The timestamp when the session was started

        You can have multiple runs for the same model, version, experiment combination.
        The idea is that you can try different configurations of a model as experiments.
        You can then execute multiple runs within the same experiment. This is especially 
        useful if you know that a run could fail.

        The use of experiments is optional, but recommended, since it makes it much easier
        to find information about configurations used to train your models.

        Parameters
        ----------
        request : object
            The incoming request data
        context : object
            The context information for the request

        Returns
        -------
        observatory.protobuf.observatory_pb2.RecordSessionStartResponse
            This method will return a response with a status code.
            The following status codes are supported:

            - 200: OK
            - 400: Bad input
            - 500: Internal error
        """
        return observatory_pb2.RecordSessionStartResponse(status=200)

    def RecordSessionCompletion(self, request, context):
        """
        This method records the completion of a training session.
        For every completion the timesetamp is recorded, so you know how long the session took to complete.

        Parameters
        ----------
        request : object
            The incoming request data
        context : object
            The context information for the request
            
        Returns
        -------
        observatory.protobuf.observatory_pb2.RecordSessionCompletionResponse
            This method will return a response with a status code.
            The following status codes are supported:

            - 200: OK
            - 400: Bad input
            - 500: Internal error
        """
        return observatory_pb2.RecordSessionCompletionResponse(status=200)