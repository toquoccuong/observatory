import time
from concurrent import futures
import grpc
from observatory.protobuf import observatory_pb2, observatory_pb2_grpc
from observatory.server.tracking_handler import TrackingServiceServicer


def run_server(port):
    """
    This method starts the RPC server for the tracking logic.
    
    Parameters
    ----------
    port : int
        The port for the server to listen on
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    observatory_pb2_grpc.add_TrackingServiceServicer_to_server(TrackingServiceServicer(), server)

    server.add_insecure_port('[::]:{}'.format(port))
    server.start()

    print('Server is listening on [::]:{}'.format(port))

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)