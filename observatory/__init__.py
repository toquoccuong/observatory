from observatory.tracking import start_run
from observatory.tracking import configure


def create_commandline_parser():
    import argparse

    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers(dest='command')

    server_parser = sub_parsers.add_parser('server', help='server --help')
    server_parser.add_argument('--port', default=5001, help='The port to listen on')
    server_parser.add_argument('--es-node', dest='seed_nodes', default=['localhost'], nargs='+')

    return parser