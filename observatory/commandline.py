import pdb

import click
import pandas as pd
from observatory.serving import ServingClient
from prettytable import PrettyTable
from tabulate import tabulate


def print_to_console(data, title):
    """
    This method prints data to command-line

    Arguments:
        data {List} -- Data thats gets printed to command line
        title {str} -- title of the data
    """

    length = 10
    for d in data:
        if len(d)> length:
            length = len(d)
    print('+' + ('-' * length) + '--+')
    print('| ' + title)
    print('+' + ('-' * length) + '--+')
    for d in data:
        print('| ' + str(d))
    print('+' + ('-' * length) + '--+')

def print_runs(params, data, r):
    """
    This method prints data to commandline
    
    Arguments:
        params {List} -- List of the parameters, ex. starttime, endtime, status
        data {List} -- List of the metrics
        r {str} -- run id
    """
    print('+' + ('-' * 115))
    print("| Run: " + r + " | StartDate: " + str(params[0][1]) + " | EndDate: " + str(params[0][2]) + " | Status: " + params[0][3])
    print('+' + ('-' * 115))
    i = 0
    for d in data:
        avg = sum(d)/len(d)
        print('| Recorded metric : ' + str(params[0][0][i]))
        print('| Highest value  : ' + str(max(d)))
        print('| Lowest value    : ' + str(min(d)))
        print('| Average value    : ' + str(round(avg, 4)))
        print('+' + ('-' * 40))
        i += 1
        

def print_comparison(left_run, right_run, r):
    """
    This method prints the compared data to command-line
    It rounds long numers to 4 digits
    
    Arguments:
        left_run {List} -- First run to compare
        right_run {List} -- Second run to compare
        metrics {List} -- List of metrics both runs have in common
        r {List} -- Run id's
    """

    print('Left is ' + r[0]+ ', Right is ' + r[1])
    print('+' + ('-' * 83) + '+')
    print('| Metric             | Highest            | Mean               | Lowest             |')
    print('+' + ('-' * 83)  + '+')
    i = 0
    for d in left_run:
        try:
            leftavg = str(round(sum(left_run[0][i])/len(left_run[0][i]), 4))
            rightavg = str(round(sum(right_run[0][i])/len(right_run[0][i]), 4))
                  # Metric name
            print('| ' + left_run[1][0][0][i] + 
                   # White Space
                  (' ' * (21 - len(left_run[1][0][0][i]))) +
                   # Max metric value
                  str(round(max(left_run[0][i]), 4)) + ' | ' + str(round(max(right_run[0][i]), 4)) + 
                   # White Space
                  (' ' * (18 - ((len(str(round(max(left_run[0][i]), 4)))) + (len(str(round(max(right_run[0][i]), 4))))))) +
                   # Avg metric value
                  leftavg + ' | ' + rightavg + 
                   # White Space
                  (' ' * (18 - ((len(str(leftavg))) + len(str(rightavg))))) +
                   # Min metric value
                  str(round(min(left_run[0][i]), 4)) + ' | ' + str(round(min(right_run[0][i]), 4)) +
                  (' ' * (16 - ((len(str(round(min(left_run[0][i]), 4)))) + len(str(round(min(right_run[0][i]), 4)))))) + '|')
            i += 1
        except IndexError:
            pass
    print('+' + ('-' * 83)  + '+')

def print_deleted_status(status):
    """
    This method prints the delete status to commandline
    
    Arguments:
        status {Boolean} -- Delete Status
    """

    if status is True:
        print('The File has been deleted succesfully')
    elif status is None:
        print('The file could not be deleted or did not exist')


@click.group()
def cli():
    pass


@cli.command(help='Runs the tracking server')
def server():
    import observatory.server


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

    Any other combination of paramaters is not valid.
    For instance, it is not possible to request a version without specifing a model
     -[INVALID] observatory get -v [VERSION_ID]

    Raises:
        AssertionError -- This gets raised when the input is wrong
    """
    serving = ServingClient()
    # ? there has to be a better way to do this
    # ? the if statement is really ugly
    if(r is not None and m is None and v is None and e is None):
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
    help='The run you want to compare -- [INPUT] = run id',
    multiple=True
)
def compare(r):
    """
    This command is used to compare the data from 2 or more runs

    It will be possible to give a model name, and it will compare all runs for that model.
    But maybe you want it to be a little more specific, so it is also possible to give a version number or experiment number.
    """
    serving = ServingClient()
    if r is not None and len(r) == 2:
        runs = []
        for x in r:
            runs.append(serving.get_run(x))
        metrics = serving.filter_metrics(runs[0][1][0][0], runs[1][1][0][0])
        if len(metrics) == 0:
            print('No common metics found')
            return
        for i in range(len(runs[0][1][0][0])):
            try:
                if runs[0][1][0][0][i] not in metrics:
                    runs[0][0].pop(i)
                    runs[0][1][0][0].pop(i)
            except IndexError:
                pass
        for i in range(len(runs[1][1][0][0])):
            try:
                if runs[1][1][0][0][i] not in metrics:
                    runs[1][0].pop(i)
                    runs[1][1][0][0].pop(i)
            except IndexError:
                pass
        print_comparison(runs[0], runs[1], metrics, r)
    else:
        print("invalid input")   
    
