import re
import tempfile
from abc import ABC, abstractmethod
import numpy as np
from itertools import chain 

import requests
from observatory import settings
from observatory.archive import Archive
from observatory.constants import LABEL_PATTERN


class ServingClient:

    def __init__(self):
        self._path = Archive.check_for_home_directory(self)

    def check_for_metrics(self, data):
        x = []
        for d in data:
            x.append(d[0])
        metrics = list(set(x))
        return metrics

    def separate_data(self, data, metrics):
        collection = []
        for m in metrics:
            mlist = []
            for d in data:
                if d[0] == m:
                    mlist.append(d[1])
            collection.append(mlist)
        return collection
        
    def structure_metrics(self, input):
        params = []
        startTime = str(input[0][4])
        input.pop(0)
        endTime = str(input[-1][1])
        status = input[-1][0]
        del input[-1]
        metrics = self.check_for_metrics(input)
        data = self.separate_data(input, metrics)
        params.append([metrics, startTime, endTime, status])
        return [data, params]

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

    def filter_metrics(self, left, right):
        metric_matches = set(left) & set(right)
        return metric_matches

    def remove_non_matches(self, data, matches):
        output = []
        for d in data:
            md = []
            for r in d:
                if any(x in matches for x in r):
                    md.append(r)
            output.append(md)
        return output                            
