import click
import pdb
from observatory.serving import ServingClient, LocalState, RemoteState 

@click.group()
def cli():
    pass


@cli.command(help='Runs the tracking server')
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
@click.option(
    '-l',
    default=None,
    help="The location where the serving module will look for the data, This can be either 'local' or 'remote'"
)
def get(m, v, e, r, l):
    serving = ServingClient()
    if(l == None):
        serving.change(LocalState)
    elif(l == 'local'):
        serving.change(LocalState)
    elif(l == 'remote'):
        serving.change(RemoteState)
    elif(l != None):
        print("Invalid location, -l shoud be either 'local' or 'remote'")
        return

    if(r != None and m == None and v == None and e == None):
        serving.get_run(r)
        print("r is not None, m is None, v is None, e is None -- succes 1")
    elif(m == None and v == None and e == None and r == None):
        serving.get_all_models()
        print("r is None, m is  None, v is None, e is none -- succes 8")
    elif(m == None or v == None and e != None and r == None):
        # raise AssertionError("wrong in put")
        print("r is None, m or v is None, v or e is not none --- fail 2")
    elif(m != None and v != None and e != None and r == None):
        experiments = serving.get_experiment(m, v, e)
        print(experiments)
        print("r is None, m is not None, v is not None, e is not none -- succes 5")
    elif(m != None and v != None and e == None and r == None):
        versions = serving.get_version(m, v)
        print(versions)
        print("r is None, m is not None, v is not None, e is none -- succes 6")
    elif (m != None and v == None and e == None and r == None):
        models = serving.get_model(m)
        print(models)
        print("r is None, m is not None, v is None, e is none -- succes 7")
    else:
        print("when trying to get model, version, or experiment, -r shouldn't be used")

@cli.command(help='Deletes the data')
def delete():
    pass

@cli.command(help='Compares the data')
def compare():
    pass