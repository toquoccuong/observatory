import click
from observatory.server import run_server


@click.group()
def cli():
    pass


@cli.command(help='Runs the tracking server')
@click.option(
    '--port',
    default=5001,
    help='The port the server should listen on for incoming tracking data. ' +
         'By default the server listens on port 5001. '
         'Please be aware that you need additional configuration on the ' +
         'client when you change the default port.')
@click.option(
    '--es-node',
    multiple=True,
    default=['localhost'],
    help='Pass in one or more ip-addresses/hostnames of elastic search' +
         ' nodes to connect to. '
         'The application will automatically try to discover more nodes, ' +
         'so in principle you need only set one node.')
def server(port, es_node):
    run_server(port, list(es_node))
