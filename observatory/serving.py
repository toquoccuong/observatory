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

    def structure_metrics(self, input):
        output = []
        startTime = str(input[0][4])
        input.pop(0)
        end = [input[-1][0], str(input[-1][1])]
        del input[-1]
        output.append([startTime, end, input])
        return output

    def get_run(self, run_id):

        if run_id.__len__() != 8:
            raise AssertionError("Invalid run id")

        run = Archive.get_run(run_id, self._path)
        return self.structure_metrics(run)

    def get_all_models(self):
        models = Archive.get_all_models(Archive, self._path)
        return models

    def get_experiment(self, model, version, experiment):
        exp = Archive.get_experiment(Archive, model, version, experiment, self._path)
        return exp

    def get_version(self, model, version):
        versions = Archive.get_version(Archive, model, version, self._path)
        return versions

    def get_model(self, model):
        mdl = Archive.get_model(Archive, model, self._path)
        return mdl

    def delete_run(self, run_id):
        return Archive.delete_run(Archive, run_id, self._path)

    def delete_experiment(self, model, version, experiment):
        return Archive.delete_experiment(model, version, experiment, self._path)

    def delete_version(self, model, version):
        return Archive.delete_version(model, version, self._path)

    def delete_model(self, model):
        return Archive.delete_model(model, self._path)

    def get_settings(self, run_id):
        return Archive.get_settings(run_id)

    def get_output(self, run_id):
        return Archive.get_output(run_id)

    def delete_settings(self, run_id):
        return Archive.delete_settings(run_id)

    def delete_output(self, run_id):
        return Archive.delete_output(run_id)

    def compare_runs(self, first_run_id, second_run_id):
        pass
