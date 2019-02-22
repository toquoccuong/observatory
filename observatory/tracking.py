from abc import ABC, abstractmethod
import json
import re
import warnings
from os import path
from time import time
from uuid import uuid4
import inspect

import requests
from observatory import settings
from observatory.constants import LABEL_PATTERN

class TrackingSession:
    #trackingsession

    def __init__(self, name, version, experiment, run_id):
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
        """
        self.name = name
        self.version = version
        self.experiment = experiment
        self.run_id = run_id
        self._state = LocalState()
    
    def change(self, state):
        self._state.switch(state)

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

        # Typechecking in python is a no-go under normal circumstances.
        # But here we're using it, because the server expects a string and float.

        if name is None or type(name) != str or name.strip() == '':
            raise AssertionError('Please provide a valid name for the metric.')

        if not re.match(LABEL_PATTERN, name):
            raise AssertionError(
                'Please provide a valid name for the metric.' +
                'it can contain lower-case alpha-numeric characters and dashes only.')

        if value is None or (type(value) != float and type(value) != int):
            raise AssertionError(
                'Please provide a valid value for the metric.')

        self._state.record_metric(
            self.name, self.version, self.experiment, self.run_id, name, value)

    def record_settings(self, **settings):
        """
        Records settings used for the run

        Parameters
        ----------
        settings : object
            A dictionary containing all settings used for the run.
            This can be passed in as `key=value` pairs.
        """
        
        if settings is None:
            warnings.warn(
                'Trying to record empty settings. ' + 
                'To prevent risk of settings loss on the server, ' +
                'the empty settings collection is discarded.', 
                RuntimeWarning)

        self._state.record_settings(
            self.name, self.version, self.experiment,
            self.run_id, dict(settings))

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

        if filename is None or filename.strip() == '':
            raise AssertionError(
                'Please provide a valid filename to store the output on the server.')

        if input_file is None or input_file.strip() == '':
            raise AssertionError(
                'Please provide a valid filename for input_file.')

        absolute_file_path = path.abspath(input_file)

        if not path.exists(absolute_file_path):
            raise AssertionError(
                f'Could not find source file {absolute_file_path} ' +
                'to upload as output of this run. Please make ' +
                'sure that the file exists on disk.')

        self._state.record_output(
            self.name, self.version, self.experiment,
            self.run_id, filename, open(absolute_file_path))

    def __enter__(self):
        self._state.record_session_start(
            self.name, self.version, self.experiment, self.run_id)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            session_status = 'COMPLETED'
        else:
            session_status = 'FAILED'

        self._state.record_session_end(
            self.name, self.version, self.experiment,
            self.run_id, session_status)


        return exc_type is None

class ObservatoryState(ABC):
    def __init__(self):
        self.n = None

    def switch(self, state):
        self.__class__ = state

    @abstractmethod
    def record_metric(self, name, value):
        """
        This method will record a metric.
        """
        pass

    @abstractmethod
    def record_settings(self, name, value):
        """
Override this method in a derived class to record a setting.
The derived class is required to store the settings as a single dictionary per run.
        """
        pass

    @abstractmethod
    def record_output(self, name, value):
        """
Override this method in a derived class to record an output for the run.
The derived class is required to handle the value of the output as an opaque binary blob.
It must not read the blob to validate it. 
        """
        pass

    @abstractmethod
    def record_session_start(self, model, version, experiment, run_id):
        """
Override this method in a derived class to record the start of a session.
The derived class is required to set the status of the run to "In progress." with a unix timestamp.
        """
        pass

    @abstractmethod
    def record_session_end(self, model, version, experiment, run_id, status):
        """
Override this method in a derived class to record the end of a session.
The derived class must, in addition to the status, also record a unix timestamp.
        """
        pass

class LocalState(ObservatoryState):
    """
    This state is used to record metadata about experiments in the current working directory using the standard data sink. 
    """

    def record_metric(self, model, version, experiment, run_id, name, value):
        #sink.save_metric(model, version, experiment, run_id, name, value)
        #localstate is nothing more than a nice data handler that passes is to sink.py
        #this is because the sever is also going to use sink.py to save data
        print("LocalState : record_metric")

    def record_settings(self, model, version, experiment, run_id, settings):
        print("LocalState : record_settings")

    def record_output(self, model, version, experiment, run_id, filename, file):
        print("LocalState : record_output")

    def record_session_start(self, model, version, experiment, run_id):
        print("LocalState : record_session_start")

    def record_session_end(self, model, version, experiment, run_id, status):
        print("LocalState : record_session_end")


class RemoteState(ObservatoryState):
    """
    Records metric on a remote server that you can run through the command `observatory server`.
    """

    def _verify_response(self, response, expected_status, expected_type='application/json'):
        """
        Verifies the response received from the tracking client against the expected status code.
        Also verifies that the method contains valid data according to the expected content_type.

        Use this method whenever your receive data from the server, to make sure that the contents
        are readable as expected.
        """
        actual_status = response.status_code
        actual_type = response.headers['Content-Type']

        if response.status_code != expected_status:
            try:
                response_content = response.json()
                error_message = response_content['message']

                raise RuntimeError('Failed to execute operation. Server returned ' +
                                   f'an error with status {actual_status}: {error_message}')
            except:
                # In some weird cases the server returns an error nobody will ever understand.
                # This catch-all fixes the problem and returns a somewhat useful error message.
                raise RuntimeError('Failed to execute operation. Server returned ' +
                                   f'an error with status: {actual_status}')

        # Sometimes the server does respond, but sends some weird piece of data that we can't parse.
        # This check makes sure that we don't try to ever read it.
        if actual_type != expected_type:
            raise RuntimeError(f'Failed to execute operation. ' +
                               'Received invalid response type: {actual_type}')

    def record_metric(self, model, version, experiment, run_id, name, value):
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
        handler_url = f'{settings.server_url}/api/models/{model}/versions/{version}/experiments/{experiment}/runs/{run_id}/metrics'
        self._verify_response(requests.post(handler_url, json={'name': name, 'value': value}), 201)

    def record_settings(self, model, version, experiment, run_id, name, value):
        print("RemoteState : record_settings")
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
        handler_url = f'{settings.server_url}/api/models/{model}/versions/{version}/experiments/{experiment}/runs/{run_id}/settings'
        self._verify_response(requests.post(handler_url, json=settings), 201)
        


    def record_output(self, model, version, experiment, run_id, filename, value):
        print("RemoteState : record_output")
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
            The response from the servers
        """
        handler_url = f'{settings.server_url}/api/models/{model}/versions/{version}/experiments/{experiment}/runs/{run_id}/outputs/{filename}'

        file_collection = {
            'file': (filename, file, 'application/octet-stream')
        }

        self._verify_response(requests.put(handler_url, files=file_collection), 201)

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
        handler_url = f'{settings.server_url}/api/models/{model}/versions/{version}/experiments/{experiment}/runs'
        self._verify_response(requests.post(handler_url, json={'run_id': run_id}), 201)

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
        handler_url = f'{settings.server_url}/api/models/{model}/versions/{version}/experiments/{experiment}/runs/{run_id}'
        self._verify_response(requests.put(handler_url, json={'status': status}), 201)

def start_run(model, version, state=LocalState(), experiment='default'):
    """
    Starts a new run for a specific model version.

    You can use this function start start recording data related to a single experiment run.
    The use of experiments is optional, you can leave this parameter out. See the example below for basic usage.

    >>> with observatory.start_run('my_model', 1, remote, experiment='my_experiment') as run:
    >>>     # Record metrics, outputs and settings

    A new run is created on the server at the start of the scope.
    It is automatically finalized at the end of the scope.

    Note that when an exception occurs within the scope of a run,
    the run is automatically marked as failed.

    Each time you invoke `start_run()` a new run is created with a newly generated UUID.
    This ensures that no runs overlap eachother.

    **Please note** it is not possible to resume a run that you started earlier.

    Parameters
    ----------
    model : string
        The name of the model
    version : int
        The version number of the model
    state : object, optinal
        The state you're working in
    experiment : string, optional
        The experiment you're working on
    """

    if model is None or model.strip() == '':
        raise AssertionError('Please provide a name for your model.')

    if not re.match(LABEL_PATTERN, model):
        raise AssertionError('name is invalid. It can contain ' +
                             'lower-case alpha-numeric characters and dashes only.')

    if experiment is None:
        experiment = 'default'

    if experiment != 'default':
        if experiment.strip() == '' or not re.match(LABEL_PATTERN, experiment):
            raise AssertionError('experiment is invalid. It can contain ' +
                                 'lower-case alpha-numeric characters and dashes only.')

    if version <= 0:
        raise AssertionError('version must be greater than zero')
    
    if state != isinstance(state, (LocalState, RemoteState)):
        raise AssertionError('State must be either a LocalState() or RemoteState()')

    run_id = str(uuid4())

    trackingSession = TrackingSession(model, version, experiment, run_id)

    trackingSession.change(state)
    
    return trackingSession
