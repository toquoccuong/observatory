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

    def structure_data(self, input):
        output = []
        for data in input:
            txt = data.split('_')
            output.append([txt[0], txt[1][1:], txt[2], txt[3][:8]])
        return output

    def structure_metrics(self, input):
        output = []
        startTime = input[0][4]
        input.pop(0)
        end = [input[-1][0], input[-1][1]]
        del input[-1]
        output.append([startTime, end, input])
        return output

    def get_run(self, run_id):
        if run_id.__len__() != 8:
            raise AssertionError("Invalid run id")
        run = Archive.get_run(run_id, self._path)
        return self.structure_metrics(run)

    def get_all_models(self):
        models = Archive.get_all_models(self._path)
        mdl = self.structure_data(models)
        just_models = []
        for m in mdl:
            just_models.append(m[0])
        unique_models = list(set(just_models))
        return unique_models

    def get_experiment(self, model, version, experiment):
        exp = Archive.get_experiment(model, version, experiment, self._path)
        return self.structure_data(exp)
    
    def get_version(self, model, version):
        versions = Archive.get_version(model, version, self._path)
        return self.structure_data(versions)

    def get_model(self, model):
        mdl = Archive.get_model(model, self._path)
        return self.structure_data(mdl)

    def delete_run(self, run_id):
        return 

    def delete_experiment(self, model, version, experiment):
        pass
    
    def delete_version(self, model, version):
        pass

    def delete_model(self, model):
        pass

    def compare_runs(self, first_run_id, second_run_id):
        pass


