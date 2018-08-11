import sys
import time
from concurrent import futures
import grpc
from observatory.protobuf import observatory_pb2, observatory_pb2_grpc
from observatory.server.tracking_handler import TrackingServiceServicer
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

    server.add_insecure_port('[::]:{}'.format(port))
    server.start()

    print('Server is started on port [::]:{}'.format(port))

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)
