import click
import pdb; 

@click.group()
def cli():
    pass


@cli.command(help='Runs the tracking server')
@click.option(
    '--port',
    default=5001,
    help='The port the server should listen on for incoming tracking data. By default the server listens on port 5001. '
         'Please be aware that you need additional configuration on the client when you change the default port.')
@click.option(
    '--es-node',
    multiple=True,
    default=['localhost'],
    help='Pass in one or more ip-addresses/hostnames of elastic search nodes to connect to. '
         'The application will automatically try to discover more nodes, so in principle you need only set one node.')
def server():
    pass

@cli.command(help='Gets the data')
@click.option(
    '-m',
    default=None,
    help='The model that should be returnd'
)
@click.option(
    '-v',
    default=None,
    help='The version of a specific model that should be returnd'
)
@click.option(
    '-e',
    default=None,
    help='An experiment of a version that should be returnd'
)
@click.option(
    '-r',
    default=None,
    help='The run that should be returnd'
)
def get(m, v, e, r):
    if(r != None and m == None and v == None and e == None):
        # return Archives.get_run(r)
        print("r is not None, m is None, v is None, e is None -- succes 1")
    elif(m == None and v == None and e == None and r == None):
        # return Archives.get_all_models()
        print("r is None, m is  None, v is None, e is none -- succes 8")
    elif(m == None or v == None and e != None and r == None):
        # raise AssertionError("wrong in put")
        print("r is None, m or v is None, v or e is not none --- fail 2")
    elif(m != None and v != None and e != None and r == None):
        # return Archives.get_experiment(m, v, e)
        print("r is None, m is not None, v is not None, e is not none -- succes 5")
    elif(m != None and v != None and e == None and r == None):
        # return Archives.get_version(m, v)
        print("r is None, m is not None, v is not None, e is none -- succes 6")
    elif (m != None and v == None and e == None and r == None):
        # return Archives.get_model(m)
        print("r is None, m is not None, v is None, e is none -- succes 7")
    else:
        print("when trying to get model, version, or experiment, -r shouldn't be used")

@cli.command(help='Deletes the data')
def delete():
    pass

@cli.command(help='Compares the data')
def compare():
    pass