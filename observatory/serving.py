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

    def delete_experiment(self, model, version, experiment):
        pass
    
    def delete_version(self, model, version):
        pass

    def delete_model(self, model):
        pass

    def compare_runs(self, first_run_id, second_run_id):
        pass
