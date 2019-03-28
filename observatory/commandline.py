import click
import pdb
from observatory.serving import ServingClient
from prettytable import PrettyTable
from tabulate import tabulate

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

    if(r != None and m == None and v == None and e == None):
        run = serving.get_run(r)
        print("| Run: " + r + " | StartDate: " + str(run[0][0]) + " | EndDate: " + str(run[0][1][1]) + " | Status: " + run[0][1][0])
        print('-' * 115)
        x = str(len(str(run[0][2][0][1])))
        print(tabulate(run[0][2], headers=['Metric', 'Value'], floatfmt="."+x+"f"))
    elif(m == None and v == None and e == None and r == None):
        models = serving.get_all_models()
        print('| Models')
        print('|------------')
        for m in models:
            print('| ' + str(m))
    elif(m == None or v == None and e != None and r == None):
        # raise AssertionError("wrong input")
        print("r is None, m or v is None, v or e is not none --- fail 2")
    elif(m != None and v != None and e != None and r == None):
        experiments = serving.get_experiment(m, v, e)
        print(tabulate(experiments, headers=['Model', 'Version', 'Experiment', 'Run'], tablefmt='orgtbl'))
    elif(m != None and v != None and e == None and r == None):
        versions = serving.get_version(m, v)
        print(tabulate(versions, headers=['Model', 'Version', 'Experiment', 'Run'], tablefmt='orgtbl'))
        print("r is None, m is not None, v is not None, e is none -- succes 6")
    elif (m != None and v == None and e == None and r == None):
        models = serving.get_model(m)
        print(tabulate(models, headers=['Model', 'Version', 'Experiment', 'Run'], tablefmt='orgtbl'))
    else:
        print("when trying to get model, version, or experiment, -r shouldn't be used")

@cli.command(help='Deletes the data')
def delete():
    pass

@cli.command(help='Compares the data')
def compare():
    pass