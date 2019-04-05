import click
import pdb
from observatory.serving import ServingClient
from prettytable import PrettyTable
from tabulate import tabulate
import pandas as pd


def print_to_console(data, title):
    """
    This method prints data to command line

    Arguments:
        data {List} -- Data thats gets printed to command line
        title {str} -- title of the data
    """

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

def print_runs(params, data, r):
    print('+' + ('-' * 115))
    print("| Run: " + r + " | StartDate: " + str(params[0][1]) + " | EndDate: " + str(params[0][2]) + " | Status: " + params[0][3])
    print('+' + ('-' * 115))
    i = 0
    for d in data:
        print('| Recorded metric : ' + str(params[0][0][i]))
        print('| Hightest value  : ' + str(max(d)))
        print('| Lowest value    : ' + str(min(d)))
        print('+' + ('-' * 40))
        i += 1
        

def print_comparison(left_run, right_run, metrics, r):
    for i in range(left_run[1][0][0].__len__()):
        try:
            if left_run[1][0][0][i] not in metrics:
                left_run[0].pop(i)
                left_run[1][0][0].pop(i)
        except IndexError:
            pass
    for i in range(right_run[1][0][0].__len__()):
        try:
            if right_run[1][0][0][i] not in metrics:
                right_run[0].pop(i)
                right_run[1][0][0].pop(i)
        except IndexError:
            pass
    print('Left is ' + r[0]+ ', Right is ' + r[1])
    print('| Metric            | Highest            | Mean               | Lowest')
    print('+' + ('-' * 80))
    i = 0
    for d in left_run:
        try:
            leftavg = str((sum(left_run[0][i])/left_run[0][i].__len__()))
            rightavg = str((sum(right_run[0][i])/right_run[0][i].__len__()))
            print('| ' + left_run[1][0][0][i] + (' ' * (20 - left_run[1][0][0][i].__len__())) + str(max(left_run[0][i])) + ' | ' + str(max(right_run[0][i])) + '       ' + leftavg + ' | ' + rightavg + '       ' + str(min(left_run[0][i])) + ' | ' + str(min(right_run[0][i])))
            i += 1
        except IndexError:
            pass

def print_deleted_status(status):
    if status is True:
        print('The File has been deleted succesfully')
    elif status is None:
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
    help='The model that should be returned -- [INPUT] = model name'
)
@click.option(
    '-v',
    default=None,
    help='The version of a specific model that should be returned -- [INPUT] = version Id'
)
@click.option(
    '-e',
    default=None,
    help='An experiment of a version that should be returned -- [INPUT] = experiment name'
)
@click.option(
    '-r',
    default=None,
    help='The run that should be returned -- [INPUT] = run id'
)
@click.option(
    '-s',
    default=None,
    help='The settings that should be returned  -- [INPUT] = run id'
)
@click.option(
    '-o',
    default=None,
    help='The output that should be returned  -- [INPUT] = run id'
)
def get(m, v, e, r, s, o):
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
    if(r is not None and m is None and v is None and e is None):
        if r.__len__() is not 8:
            print('[ERROR]: Invalid run id, it must be 8 characters long')
        else:
            run = serving.get_run(r)
            print_runs(run[1], run[0], r)
        return
    if(o is not None and m is None and v is None and e is None and r is None and s is None):
        output = serving.get_output(o)
        print(output)
        return
    if(s is not None and m is None and v is None and e is None and r is None and o is None):
        settings = serving.get_settings(s)
        print(settings)
        return
    elif(m is None and v is None and e is None and r is None and o is None and s is None):
        models = serving.get_all_models()
        print_to_console(models, 'Models')
        return
    elif(m is None or v is None and e is not None and r is None):
        print("[ERROR]: The given input is invalid")
        return
    elif(m is not None and v is not None and e is not None and r is None and o is None and s is None):
        experiments = serving.get_experiment(m, v, e)
        print_to_console(experiments, 'Runs')
        return
    elif(m is not None and v is not None and e is None and r is None and o is None and s is None):
        versions = serving.get_version(m, v)
        print_to_console(versions, 'Experiments')
        return
    elif (m is not None and v is None and e is None and r is None and o is None and s is None):
        models = serving.get_model(m)
        print_to_console(models, 'Versions')
        return
    else:
        print("[ERROR]: when trying to get model, version, or experiment, no other parameters should be used")
        return


@cli.command(help='Deletes the data')
@click.option(
    '-m',
    default=None,
    help='The model that should be deleted -- [INPUT] = model name'
)
@click.option(
    '-v',
    default=None,
    help='The version of a specific model that should be deleted -- [INPUT] = verion id'
)
@click.option(
    '-e',
    default=None,
    help='An experiment of a version that should be deleted -- [INPUT] = experiment name'
)
@click.option(
    '-r',
    default=None,
    help='The run that should be deleted -- [INPUT] = run id'
)
@click.option(
    '-s',
    default=None,
    help='The settings that should be deleted  -- [INPUT] = run id'
)
@click.option(
    '-o',
    default=None,
    help='The output that should be deleted  -- [INPUT] = run id'
)
def delete(m, v, e, r, s, o):
    """
    For the Delete module there are five possible valid commands.

    - observatory delete
        This command has no paramaters, and returns a list of all models

    - observatory delete -m [MODEL_NAME]
        It will delete the model

    - observatory delete -m [MODEL_NAME] -v [VERSION_ID]
        This command will delete a specified version

    - obsrevatory delete -m [MODEL_NAME] -v [VERSION_ID] -e [EXPERIMENT_NAME]
        This command will delete a specified experiment

    - observatory delete -r [RUN_ID]
        This command deletes the metadata for a specific run.

    Any other combination of paramaters is not valid.
    For instance, it is not possible to delete a version without specifing a model
     -[INVALID] observatory delete -v [VERSION_ID]

    Raises:
        AssertionError -- This gets raised when the input is wrong
    """
    serving = ServingClient()
    if(r is not None and m is None and v is None and e is None and o is None and s is None):
        if click.confirm('Are you sure you want to delete this?'):
            print_deleted_status(serving.delete_run(r))
        return
    if(o is not None and m is None and v is None and e is None and r is None and s is None):
        if click.confirm('Are you sure you want to delete this?'):
            print_deleted_status(serving.delete_output(o))
        return
    if(s is not None and m is None and v is None and e is None and r is None and o is None):
        if click.confirm('Are you sure you want to delete this?'):
            print_deleted_status(serving.delete_settings(s))
        return
    elif(m is None and v is None and e is None and r is None and o is None and s is None):
        # ? delete everyting
        pass
    elif(m is None or v is None and e is not None and r is None and o is None and s is None):
        print("The given input is invalid")
        return
    elif(m is not None and v is not None and e is not None and r is None and o is None and s is None):
        if click.confirm('Are you sure you want to delete this?'):
            print_deleted_status(serving.delete_experiment(m, v, e))
        return
    elif(m is not None and v is not None and e is None and r is None and o is None and s is None):
        if click.confirm('Are you sure you want to delete this?'):
            print_deleted_status(serving.delete_version(m, v))
        return
    elif (m is not None and v is None and e is None and r is None and o is None and s is None):
        if click.confirm('Are you sure you want to delete this?'):
            print_deleted_status(serving.delete_model(m))
        return
    else:
        print("when trying to get model, version, or experiment, -r shouldn't be used")
        return


@cli.command(help='Compares the data')
@click.option(
    '-r',
    default=None,
    help='The run that should be deleted -- [INPUT] = run id',
    multiple=True
)
def compare(r):
    """
    This command is used to compare the data from 2 or more runs

    It will be possible to give a model name, and it will compare all runs for that model.
    But maybe you want it to be a little more specific, so it is also possible to give a version number or experiment number.
    """
    serving = ServingClient()
    if r is not None and r.__len__() == 2:
        runs = []
        for x in r:
            runs.append(serving.get_run(x))
        metrics = serving.filter_metrics(runs[0][1][0][0], runs[1][1][0][0])
        print_comparison(runs[0], runs[1], metrics, r)
    else:
        print("invalid input")   
    
