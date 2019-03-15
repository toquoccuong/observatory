import json
from os import path, makedirs
from observatory.utils import index_name
from observatory import settings



def configure(path):
    """
    Configures the tracking sink to save the data in a specific folder

    Parameters
    ---------
    path : string
        The path to the specified location
    """
    

def record_metric(model, version, experiment, run_id, timestamp, metric_name, metric_value):
    """
    Records a metric value.

    This method records a single metric value for a run. 

    Parameters
    ----------
    run_id : string
        The ID of the run
    timestamp : long
        The timestamp for the metric value
    metric_name : string
        The name of the metric
    metric_value : float
        The value of the metric
    """


def record_session_start(model, version, experiment, run_id, timestamp):
    """
    Records the start of a session

    When you start a new run, this method gets called to record the start of the session.
    After you've started a session you can record its final status and completion time with record_session_end.

    Parameters
    ----------
    model : string
        The name of the model
    version : int
        The version number of the model
    experiment : string
        The name of the experiment
    run_id : string
        The ID of the run
    timestamp : int
        The timestamp
    """
    


def record_session_end(status):
    """
    Records the end of a tracking session

    When you've started tracking a run with record_session_start you can call this method to signal
    the completion of the run. This updates the existing run document with the completion time
    and status of the run.

    Please note that this function raises an error when you try to complete a run that wasn't started earlier.
    This is done to prevent the tool from recording "empty" sessions.

    Parameters
    ----------
    status : str
        The status of the run (completed, failed)
    """


def record_settings(model, version, experiment, run_id, settings):
    """
    Records the settings used for a particular experiment run.

    When you record settings, you have to record all settings at once. There is
    no automatic merging of settings by this method.

    Parameters:
    -----------
    model : str
        The name of the model
    version : int
        The model version
    experiment : str
        The name of the experiment
    run_id : str
        The identifier for the run
    settings : dict
        The settings to record on disk
    """


def record_output(model, version, experiment, run_id, filename, file):
    """
    Records the output for an experiment

    The output file is stored as part of the run. It is stored as-is without 
    any checks on the extension or file contents. 

    Parameters:
    -----------
    model : str
        The name of the model
    version : int
        The model version
    experiment : str
        The name of the experiment
    run_id : str
        The identifier for the run
    filename : str
        The filename of the file
    file : object
        The file handle
    """
