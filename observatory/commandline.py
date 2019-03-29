import click
import pdb
from observatory.serving import ServingClient
from prettytable import PrettyTable
from tabulate import tabulate

def print_to_console(data, title):
    length = 10
    for d in data:
        if d.__len__() > length:
            length = d.__len__()
    print('+' + ('-' * length) + '----+')
    print('| ' + title)
    print('+' + ('-' * length) + '----+')
    for d in data:
        print('| ' + str(d))
    print('+' + ('-' * length) + '----+')

def print_deleted_status(status):
    if status == True:
        print('The File has been deleted succesfully')
    elif status == None:
        print('The file could not be deleted or did not exist')

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
    help='The model that should be returned'
)
@click.option(
    '-v',
    default=None,
    help='The version of a specific model that should be returned'
)
@click.option(
    '-e',
    default=None,
    help='An experiment of a version that should be returned'
)
@click.option(
    '-r',
    default=None,
    help='The run that should be returned'
)
def get(m, v, e, r):
    """
    For the get module there are five possible valid commands.

    - observatory get
        This command has no paramaters, and returns a list of all models

    - observatory get -m [MODEL_NAME]
        This command takes one paramater, the model name.
        It will return a list of all versions associated with the model

    - observatory get -m [MODEL_NAME] -v [VERSION_ID]
        This command will return a list with all experiments for a specified version

    - obsrevatory get -m [MODEL_NAME] -v [VERSION_ID] -e [EXPERIMENT_NAME]
        This command will return a list with all runs for a specified experiment

    - observatory get -r [RUN_ID]
        This command returns the metadata for a specific run.
        It will show the highest found value, the lowest found value
        # ? need to look at pandas how they deal with commands line data

    Any other combination of paramaters is not valid.
    For instance, it is not possible to request a version without specifing a model
     -[INVALID] observatory get -v [VERSION_ID]
    
    
    Raises:
        AssertionError -- This gets raised when the input is wrong
    """
    serving = ServingClient()
    if(r != None and m == None and v == None and e == None):
        run = serving.get_run(r)
        print("| Run: " + r + " | StartDate: " + str(run[0][0]) + " | EndDate: " + str(run[0][1][1]) + " | Status: " + run[0][1][0])
        print('-' * 115)
        x = str(len(str(run[0][2][0][1])))
        print(tabulate(run[0][2], headers=['Metric', 'Value'], floatfmt="."+x+"f"))
    elif(m == None and v == None and e == None and r == None):
        models = serving.get_all_models()
        print_to_console(models, 'Models')
    elif(m == None or v == None and e != None and r == None):
        raise AssertionError("wrong input")
    elif(m != None and v != None and e != None and r == None):
        experiments = serving.get_experiment(m, v, e)
        print_to_console(experiments, 'Runs')
    elif(m != None and v != None and e == None and r == None):
        versions = serving.get_version(m, v)
        print_to_console(versions, 'Experiments')
    elif (m != None and v == None and e == None and r == None):
        models = serving.get_model(m)
        print_to_console(models, 'Versions')
    else:
        print("when trying to get model, version, or experiment, -r shouldn't be used")

@cli.command(help='Deletes the data')
@click.option(
    '-m',
    default=None,
    help='The model that should be deleted'
)
@click.option(
    '-v',
    default=None,
    help='The version of a specific model that should be deleted'
)
@click.option(
    '-e',
    default=None,
    help='An experiment of a version that should be deleted'
)
@click.option(
    '-r',
    default=None,
    help='The run that should be deleted'
)
def delete(m, v, e, r):
    serving = ServingClient()
    if(r != None and m == None and v == None and e == None):
        if click.confirm('Are you sure you want to delete this?'):
            print_deleted_status(serving.delete_run(r))
    elif(m == None and v == None and e == None and r == None):
        # ? delete everyting
        pass
    elif(m == None or v == None and e != None and r == None):
        raise AssertionError("wrong input")
    elif(m != None and v != None and e != None and r == None):
        if click.confirm('Are you sure you want to delete this?'):
            print_deleted_status(serving.delete_experiment(m, v, e))
    elif(m != None and v != None and e == None and r == None):
        if click.confirm('Are you sure you want to delete this?'):
            print_deleted_status(serving.delete_version(m, v))
    elif (m != None and v == None and e == None and r == None):
        if click.confirm('Are you sure you want to delete this?'):
            print_deleted_status(serving.delete_model(m))
    else:
        print("when trying to get model, version, or experiment, -r shouldn't be used")

@cli.command(help='Compares the data')
def compare():
    pass