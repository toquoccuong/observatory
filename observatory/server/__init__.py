import sys
import time
from concurrent import futures
import grpc
from observatory.protobuf import observatory_pb2, observatory_pb2_grpc
from observatory.server.handlers import TrackingServiceServicer, ModelServiceServicer
import observatory.sink as tracking_sink


def run_server(port, elasticsearch_nodes):
    """
    This method starts the RPC server for the tracking logic.
    
    Parameters
    ----------
    port : int
        The port for the server to listen on
    elasticsearch_nodes : [string]
        The list of nodes that the server should connect to for tracking the metrics and other model data.
    """

    tracking_sink.configure(elasticsearch_nodes)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    observatory_pb2_grpc.add_TrackingServiceServicer_to_server(TrackingServiceServicer(), server)
    observatory_pb2_grpc.add_ModelServiceServicer_to_server(ModelServiceServicer(), server)

    server.add_insecure_port('[::]:{}'.format(port))
    server.start()

    print('server is listening on [::]:{}'.format(port))

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)
