from abc import ABC, abstractmethod
import json
import re
import warnings
from os import path
from time import time
from uuid import uuid4
import inspect
import pdb

import requests
from observatory import settings
from observatory.constants import LABEL_PATTERN
from benchmarks import benchmark_local_saving


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
        self._state = LocalState_text()
    
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
    def record_settings(self, settings):
        """
        Override this method in a derived class to record a setting.
        The derived class is required to store the settings as a single dictionary per run.
        """
        pass

    @abstractmethod
    def record_output(self, input_file, filename):
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

class LocalState_text(ObservatoryState):
    """
    This state is used to record metadata about experiments in the current working directory using the standard data sink. 
    """

    def record_metric(self, model, version, experiment, run_id, name, value):
        benchmark_local_saving.benchmark_text.record_metric(self, model, version, experiment, run_id, name, value)

    def record_session_start(self, model, version, experiment, run_id):
        benchmark_local_saving.benchmark_text.record_session_start(self, model, version, experiment, run_id)

    def record_session_end(self, model, version, experiment, run_id, status):
        benchmark_local_saving.benchmark_text.record_session_end(self, model, version, experiment, run_id, 'completed')

    def record_settings(self, settings):
        pass

    def record_output(self, input_file, filename):
        pass

class LocalState_null(ObservatoryState):
    """
    This state is used to record metadata about experiments in the current working directory using the standard data sink. 
    """

    def record_metric(self, model, version, experiment, run_id, name, value):
        pass

    def record_session_start(self, model, version, experiment, run_id):
        pass

    def record_session_end(self, model, version, experiment, run_id, status):
        pass

    def record_settings(self, settings):
        pass

    def record_output(self, input_file, filename):
        pass

class LocalState_json(ObservatoryState):
    """
    This state is used to record metadata about experiments in the current working directory using the standard data sink. 
    """

    def record_metric(self, model, version, experiment, run_id, name, value):
        benchmark_local_saving.benchmark_JSON.record_metric(self, model, version, experiment, run_id, name, value)

    def record_session_start(self, model, version, experiment, run_id):
        
        benchmark_local_saving.benchmark_JSON.record_session_start(self, model, version, experiment, run_id)

    def record_session_end(self, model, version, experiment, run_id, status):
        benchmark_local_saving.benchmark_JSON.record_session_end(self, model, version, experiment, run_id, 'completed')        

    def record_settings(self, settings):
        pass

    def record_output(self, input_file, filename):
        pass

class LocalState_pickle(ObservatoryState):
    """
    This state is used to record metadata about experiments in the current working directory using the standard data sink. 
    """

    def record_metric(self, model, version, experiment, run_id, name, value):
        benchmark_local_saving.benchmark_pickle.record_metric(self, model, version, experiment, run_id, name, value)
        
    def record_session_start(self, model, version, experiment, run_id):
        benchmark_local_saving.benchmark_pickle.record_session_start(self, model, version, experiment, run_id)

    def record_session_end(self, model, version, experiment, run_id, status):
        benchmark_local_saving.benchmark_pickle.record_session_end(self, model, version, experiment, run_id, 'completed')

    def record_settings(self, settings):
        pass

    def record_output(self, input_file, filename):
        pass

class LocalState_cpickle(ObservatoryState):
    """
    This state is used to record metadata about experiments in the current working directory using the standard data sink. 
    """

    def record_metric(self, model, version, experiment, run_id, name, value):
        benchmark_local_saving.benchmark_cpickle.record_metric(self, model, version, experiment, run_id, name, value)

    def record_session_start(self, model, version, experiment, run_id):
        benchmark_local_saving.benchmark_cpickle.record_session_start(self, model, version, experiment, run_id)

    def record_session_end(self, model, version, experiment, run_id, status):
        benchmark_local_saving.benchmark_cpickle.record_session_end(self, model, version, experiment, run_id, 'completed')

    def record_settings(self, settings):
        pass

    def record_output(self, input_file, filename):
        pass
    
class LocalState_sqlite(ObservatoryState):
    """
    This state is used to record metadata about experiments in the current working directory using the standard data sink. 
    """

    def record_metric(self, model, version, experiment, run_id, name, value):
        benchmark_local_saving.benchmark_sqlite.record_metric(self, model, version, experiment, run_id, name, value)

    def record_session_start(self, model, version, experiment, run_id):
        benchmark_local_saving.benchmark_sqlite.record_session_start(self, model, version, experiment, run_id)

    def record_session_end(self, model, version, experiment, run_id, status):
        benchmark_local_saving.benchmark_sqlite.record_session_end(self, model, version, experiment, run_id, 'completed')

    def record_settings(self, settings):
        pass

    def record_output(self, input_file, filename):
        pass

class LocalState_pytables(ObservatoryState):
    """
    This state is used to record metadata about experiments in the current working directory using the standard data sink. 
    """

    def record_metric(self, model, version, experiment, run_id, name, value):
        benchmark_local_saving.benchmark_pytables.record_metric(self, model, version, experiment, run_id, name, value)
    def record_session_start(self, model, version, experiment, run_id):
        benchmark_local_saving.benchmark_pytables.record_session_start(self, model, version, experiment, run_id)

    def record_session_end(self, model, version, experiment, run_id, status):
        benchmark_local_saving.benchmark_pytables.record_session_end(self, model, version, experiment, run_id, 'completed')

    def record_settings(self, settings):
        pass

    def record_output(self, input_file, filename):
        pass

def start_run(model, version, state, experiment='default'):
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
    
    run_id = str(uuid4())

    trackingSession = TrackingSession(model, version, experiment, run_id)
    trackingSession.change(state)

    return trackingSession
