import re
import tempfile
from abc import ABC, abstractmethod

import requests
from observatory import settings
from observatory.archive import Archive
from observatory.constants import LABEL_PATTERN

class ServingClient:
    
    def __init__(self):
        self._path = Archive.check_for_home_directory(self)
        self._state = LocalState()

    def change(self, state):
        """
        Needed for the implementation of the state pattern, with this it is possilbe
        to switch betweeen states.
        
        Arguments:
            state {LocalState or RemoteState} -- The current state of the TrackingSession
        """
        self._state.switch(state)

    # all methods
    def get_run(self, run_id):
        if run_id is None:
            raise AssertionError("no valid run id")

        return self._state.get_run(run_id)

    def get_all_models(self):
        return self._state.get_all_models()

    def get_experiment(self, model, version, experiment):
        return self._state.get_experiment(model, version, experiment, self._path)
    
    def get_version(self, model, version):
        return self._state.get_version(model, version, self._path)

    def get_model(self, model):
        return self._state.get_model(model, self._path)

    def delete_run(self, run_id):
        return self._state.delete_run(run_id)

    def delete_all_models(self):
        # ? not sure if this should be a method
        return self._state.delete_all_models()

    def delete_experiment(self, model, version, experiment):
        return self._state.delete_experiment(model, version, experiment)
    
    def delete_version(self, model, version):
        return self._state.delete_version(model, version)

    def delete_model(self, model):
        return self._state.delete_model(model)

    def compare_runs(self, first_run_id, second_run_id):
        return self._state.compare_runs(first_run_id, second_run_id)

class ServingState(ABC):

    def __init__(self):
        self.n = None

    def switch(self, state):
        self.__class__ = state

    @abstractmethod
    def get_run(self, run_id):
        """
        Override this method in a derived class.
        """
        pass

    @abstractmethod
    def get_all_models(self):
        """
        Override this method in a derived class.
        """
        pass

    @abstractmethod
    def get_experiment(self, model, version, experiment, path):
        """
        Override this method in a derived class.
        """
        pass
    
    @abstractmethod
    def get_version(self, model, version, path):
        """
        Override this method in a derived class.
        """
        pass

    @abstractmethod
    def get_model(self, model, path):
        """
        Override this method in a derived class.
        """
        pass

    @abstractmethod
    def delete_run(self, run_id):
        """
        Override this method in a derived class.
        """
        pass

    @abstractmethod
    def delete_all_models(self):
        """
        Override this method in a derived class.
        """
        # ? not sure if this should be a method
        pass

    @abstractmethod
    def delete_experiment(self, model, version, experiment):
        """
        Override this method in a derived class.
        """
        pass
    
    @abstractmethod
    def delete_version(self, model, version):
        """
        Override this method in a derived class.
        """
        pass

    @abstractmethod
    def delete_model(self, model):
        """
        Override this method in a derived class.
        """
        pass

    @abstractmethod
    def compare_runs(self, first_run_id, second_run_id):
        """
        Override this method in a derived class.
        """
        pass

class LocalState(ServingState):

    def get_run(self, run_id):
        Archive.get_run(run_id)

    def get_all_models(self):
        pass

    def get_experiment(self, model, version, experiment, path):
        return Archive.get_experiment(self, model, version, experiment, path)
    
    def get_version(self, model, version, path):
        return Archive.get_version(self, model, version, path)

    def get_model(self, model, path):
        return Archive.get_model(self, model, path)

    def delete_run(self, run_id):
        pass

    def delete_all_models(self):
        # ? not sure if this should be a method
        pass

    def delete_experiment(self, model, version, experiment):
        pass
    
    def delete_version(self, model, version):
        pass

    def delete_model(self, model):
        pass

    def compare_runs(self, first_run_id, second_run_id):
        pass

class RemoteState(ServingState):
    
    def get_run(self, run_id):
        pass

    def get_all_models(self):
        pass

    def get_experiment(self, model, version, experiment):
        pass
    
    def get_version(self, model, version):
        pass

    def get_model(self, model):
        pass

    def delete_run(self, run_id):
        pass

    def delete_all_models(self):
        # ? not sure if this should be a method
        pass

    def delete_experiment(self, model, version, experiment):
        pass
    
    def delete_version(self, model, version):
        pass

    def delete_model(self, model):
        pass

    def compare_runs(self, first_run_id, second_run_id):
        pass
