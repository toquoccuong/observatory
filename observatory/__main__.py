import argparse


parser = argparse.ArgumentParser(description='Machine Learning Model Management Tool')
sub_parsers = parser.add_subparsers(dest='command')

server_parser = sub_parsers.add_parser('server', help='server --help')
server_parser.add_argument('--port', default=5001, help='The port to listen on')

args = parser.parse_args()

if args.command == 'server':
    import observatory.server
    observatory.server.run_server(args.port)