"""
The tracking module is used to record various parts of your machine learning runs.
You can use the :func:`start_run <observatory.tracking.start_run>` method from 
this module to start tracking metrics, outputs and settings for your 
machine learning runs.

If you want to customize tracking behavior you can create your own instance
of :class:`TrackingClient <observatory.tracking.TrackingClient>` to send 
information to the tracking API directly. Please note that this means you have 
to implement session semantics yourself.
"""

import json
import re
from concurrent import futures
from time import time
from uuid import uuid4

import requests
from observatory import settings
from observatory.constants import LABEL_PATTERN


class TrackingClient:
    """
    Implements logic to convert raw data into HTTP requests to the tracking endpoint.

    Typically you should not be using this class in your own code. Instead make use of the `start_run` method
    in the same module to start a new tracking session. This ensures correct tracking behavior in your application.

    This client is meant as a wrapper around all the HTTP related logic from the tracking session's point of view.
    """

    def __init__(self, url):
        """
        Initializes a new instance of the tracking client

        Parameters:
        -----------
        url : str
            The URL of the tracking endpoint to communicate with
        """
        self.url = url

    def record_session_start(self, model, version, experiment, run_id):
        """
        Records the start of a session.

        This method sends a HTTP request with the right payload to the observatory tracking endpoint.
        The result is a 201 when the server succesfully recorded the session completion. Otherwise
        the server will return a 500 response.

        Parameters:
        -----------
        model : str
            The name of the model
        version : int
            The version of the model
        experiment : str
            The name of the experiment
        run_id : str
            The identifier for the run

        Returns:
        --------
        requests.Response
            The response from the server
        """
        handler_url = f'{self.url}/api/models/{model}/versions/{version}/experiments/{experiment}/runs'
        return requests.post(handler_url, json={'run_id': run_id})

    def record_settings(self, model, version, experiment, run_id, settings):
        """
        Records the settings of an experiment run.

        This method sends a HTTP request with the right payload to the observatory tracking endpoint.
        The result is a 201 when the server succesfully recorded the session completion. Otherwise
        the server will return a 500 response.

        Parameters:
        -----------
        model : str
            The name of the model
        version : int
            The version of the model
        experiment : str
            The name of the experiment
        run_id : str
            The identifier for the run
        settings : dict
            The dictionary with run settings

        Returns:
        --------
        requests.Response
            The response from the server
        """
        handler_url = f'{self.url}/api/models/{model}/versions/{version}/experiments/{experiment}/runs/{run_id}/settings'
        return requests.post(handler_url, json=settings)

    def record_metric(self, model, version, experiment, run_id, metric_name, metric_value):
        """
        Records a metric during a run.

        This method sends a HTTP request with the right payload to the observatory tracking endpoint.
        The result is a 201 when the server succesfully recorded the session completion. Otherwise
        the server will return a 500 response.

        Parameters:
        -----------
        model : str
            The name of the model
        version : int
            The version of the model
        experiment : str
            The name of the experiment
        run_id : str
            The identifier for the run
        metric_name : str
            The name of the metric
        metric_value : str
            The value of the metric

        Returns:
        --------
        requests.Response
            The response from the server
        """
        handler_url = f'{self.url}/api/models/{model}/versions/{version}/experiments/{experiment}/runs/{run_id}/metrics'
        return requests.post(handler_url, json={'name': metric_name, 'value': metric_value})

    def record_output(self, model, version, experiment, run_id, filename, file):
        """
        Records an output of an experiment run

        This method sends a HTTP request with the right payload to the observatory tracking endpoint.
        The result is a 201 when the server succesfully recorded the session completion. Otherwise
        the server will return a 500 response.

        Parameters:
        -----------
        model : str
            The name of the model
        version : int
            The version of the model
        experiment : str
            The name of the experiment
        run_id : str
            The identifier for the run
        filename : str
            The filename of the output
        file : object
            The file handle to use for reading the output data

        Returns:
        --------
        requests.Response
            The response from the server
        """
        handler_url = f'{self.url}/api/models/{model}/versions/{version}/experiments/{experiment}/runs/{run_id}/outputs/{filename}'

        file_collection = {
            'file': (filename, file, 'application/octet-stream')
        }

        return requests.put(handler_url, files=file_collection)

    def record_session_end(self, model, version, experiment, run_id, status):
        """
        Records the end of a session.

        This method sends a HTTP request with the right payload to the observatory tracking endpoint.
        The result is a 201 when the server succesfully recorded the session completion. Otherwise
        the server will return a 500 response.

        Parameters:
        -----------
        model : str
            The name of the model
        version : int
            The version of the model
        experiment : str
            The name of the experiment
        run_id : str
            The identifier for the run
        status : str
            The status of the run

        Returns:
        --------
        requests.Response
            The response from the server
        """
        handler_url = f'{self.url}/api/models/{model}/versions/{version}/experiments/{experiment}/runs/{run_id}'
        return requests.put(handler_url, json={'status': status})


class TrackingSession:
    """
    The tracking session is used to track data related to a single training run.

    When you invoke :func:`start_run <observatory.start_run>` this class is instantiated for you
    with the correct settings to start tracking data.

    Any server connection used by the tracking logic is automatically opened and closed for you.
    """

    def __init__(self, name, version, experiment, run_id, tracking_client):
        """
        Initializes the tracking session with the necessary tracking information
        and a pre-initialized tracking client for recording the actual metrics.

        Parameters
        ----------
        name : string
            Name of the model
        version : int
            Version number of the model
        experiment : string
            Name of the experiment
        run_id : string
            ID of the run
        tracking_client : object
            Instance of the tracking service client
        """
        self.name = name
        self.version = version
        self.run_id = run_id
        self.tracking_client = tracking_client
        self.experiment = experiment

    def record_metric(self, name, value):
        """
        Records a metric value on the server

        Parameters
        ----------
        name : string
            The name of the metric to record
        value : float
            The value of the metric to records
        """
        response = self.tracking_client.record_metric(
            self.name, self.version, self.experiment, self.run_id, name, value)

        if response.status_code != 201:
            raise RuntimeError('Failed to record metric')

    def record_settings(self, **settings):
        """
        Records settings used for the run

        Parameters
        ----------
        settings : object
            A dictionary containing all settings used for the run.
            This can be passed in as `key=value` pairs.
        """
        response = self.tracking_client.record_settings(
            self.name, self.version, self.experiment,
            self.run_id, dict(settings))

        if response.status_code != 201:
            raise RuntimeError('Failed to record settings')

    def record_output(self, input_file, filename):
        """
        Records an output for the current run.

        Parameters
        ----------
        input_file : object
            Filename or handle to input file
        filename : string
            Name of the file as it should be stored on the server
        """

        response = self.tracking_client.record_output(
            self.name, self.version, self.experiment,
            self.run_id, filename, open(filename))

        if response.status_code != 201:
            raise RuntimeError('Failed to record output')

    def __enter__(self):
        response = self.tracking_client.record_session_start(
            self.name, self.version, self.experiment, self.run_id)

        if response.status_code != 201:
            raise RuntimeError('Failed to record session start')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            session_status = 'COMPLETED'
        else:
            session_status = 'FAILED'

        response = self.tracking_client.record_session_end(
            self.name, self.version, self.experiment,
            self.run_id, session_status)

        if response.status_code != 201:
            raise RuntimeError('Failed to record session completion')

        return exc_type is None


def start_run(model, version, experiment='default'):
    """
    Starts a new run for a specific model version.

    You can use this function start start recording data related to a single experiment run.
    The use of experiments is optional, you can leave this parameter out. See the example below for basic usage.

    >>> with observatory.start_run('my_model', 1, experiment='my_experiment') as run:
    >>>     # Record metrics, outputs and settings

    A new run is created on the server at the start of the scope.
    It is automatically finalized at the end of the scope.

    Note that when an exception occurs within the scope of a run,
    the run is automatically marked as failed.

    Each time you invoke `start_run` a new run is created with a newly generated UUID.
    This ensures that no runs overlap eachother.

    **Please note** it is not possible to resume a run that you started earlier.

    Parameters
    ----------
    model : string
        The name of the model
    version : int
        The version number of the model
    experiment : string, optional
        The experiment you're working on
    """

    if not re.match(LABEL_PATTERN, model):
        raise AssertionError('name is invalid. It can contain ' +
                             'lower-case alpha-numeric characters and dashes only.')

    if experiment is None:
        experiment = 'default'

    if experiment != 'default' and not re.match(LABEL_PATTERN, model):
        raise AssertionError('experiment is invalid. It can contain ' +
                             'lower-case alpha-numeric characters and dashes only.')

    if version <= 0:
        raise AssertionError('version must be greater than zero')

    run_id = str(uuid4())
    tracking_client = TrackingClient(settings.server_url)

    return TrackingSession(model, version, experiment, run_id, tracking_client)
