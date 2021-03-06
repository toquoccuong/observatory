from os import path, listdir, makedirs
import os
from os.path import expanduser
from fnmatch import fnmatch as match
import json
import tempfile
import tarfile
import pickle


class Archive:

    def structure_data(input, index):
        output = []
        for data in input:
            txt = data.split('_')
            if index == 0:
                output.append(txt[0])
            elif index == 1:
                output.append(txt[1][1:])
            elif index == 2:
                output.append(txt[2])
            elif index == 3:
                output.append(txt[3][:8])
        return output

    @staticmethod
    def check_for_home_directory(self):
        # this module depends on the .observatory directory.
        # So we need to make sure it exists.
        home = expanduser("~")
        if os.path.exists(home + "\\.observatory"):
            # if it exists the path will be set
            self._path = (home + "\\.observatory\\metrics")
            return self._path
        elif os.path.exists("\\.observatory"):
            self._path = ("\\.observatory\\")
            return self._path
        else:
            print("no home directory found")

    @staticmethod
    def get_run(run_id, path):
        metrics = []
        for file in os.listdir(path):
            if '_' + run_id + '-' in file:
                with open(path + '\\' + file, 'rb') as f:
                    while True:
                        try:
                            metrics.append(pickle.load(f))
                        except EOFError:
                            break
        return metrics

    @staticmethod
    def get_all_models(self, path):
        models = []
        for file in os.listdir(path):
                models.append(file)
        just_models = self.structure_data(models, 0)
        return list(set(just_models))

    @staticmethod
    def get_model(self, model, path):
        """
        Gets the requested model

        Does not have to be perfecht match

        Arguments:
            model {str} -- model name
            path {str} -- Path to file destination

        Returns:
            list -- list of all found versions for the input model,
        """

        models = []
        for file in os.listdir(path):
            if model + '_' in file:
                models.append(file)
        just_models = self.structure_data(models, 1)
        return list(set(just_models))

    @staticmethod
    def get_version(self, model, version, path):
        """
        Gets the requested experiments

        version has to be perfecht match

        Arguments:
            model {str} -- model name
            version {str} -- version number
            path {str} -- Path to file destination

        Returns:
            list -- list of all found experiments
        """
        versions = []
        for file in os.listdir(path):
            if model in file:
                if '_v' + version + '_' in file:
                    versions.append(file)
        just_versions = self.structure_data(versions, 2)
        return list(set(just_versions))

    @staticmethod
    def get_experiment(self, model, version, experiment, path):
        """
        Gets the requested runs

        Arguments:
            model {str} -- model name
            version {str} -- version number
            path {str} -- Path to file destination

        Returns:
            list -- list of all found runs
        """
        experiments = []
        for file in os.listdir(path):
            if model + '_' in file:
                if '_v' + version + '_' in file:
                    if '_' + experiment + '_' in file:
                        experiments.append(file)
        just_experiments = self.structure_data(experiments, 3)
        return list(set(just_experiments))

    @staticmethod
    def delete_run(self, run_id, path):
        for file in os.listdir(path):
            if '_' + run_id + '-' in file:
                os.remove(path + '\\' + file)
                return True

    @staticmethod
    def delete_experiment(model, version, experiment, path):
        for file in os.listdir(path):
            if model + '_' in file:
                if '_v' + version + '_' in file:
                    if '_' + experiment + '_' in file:
                        os.remove(path + '\\' + file)
                        return True

    @staticmethod
    def delete_version(model, version, path):
        for file in os.listdir(path):
            if model in file:
                if '_v' + version + '_' in file:
                    os.remove(path + '\\' + file)
                    return True

    @staticmethod
    def delete_model(model, path):
        for file in os.listdir(path):
            if model + '_' in file:
                os.remove(path + '\\' + file)
                return True

    @staticmethod
    def get_settings(run_id):
        home = expanduser('~')
        if os.path.exists(home + "\\.observatory"):
            path = home + "\\.observatory\\settings\\"
        else:
            return
        settings = []
        for file in os.listdir(path):
            if '_' + run_id + '-' in file:
                with open(path + '\\' + file, 'rb') as f:
                    while True:
                        try:
                            settings.append(pickle.load(f))
                        except EOFError:
                            break
        return settings        

    @staticmethod
    def delete_settings(run_id):
        home = expanduser('~')
        if os.path.exists(home + "\\.observatory"):
            path = home + "\\.observatory\\settings\\"
        else:
            return False

        for file in os.listdir(path):
            if '_' + run_id + '-' in file:
                os.remove(path + file)
                return True
           
    @staticmethod
    def get_output(run_id):
        home = expanduser('~')
        if os.path.exists(home + "\\.observatory"):
            path = home + "\\.observatory\\outputs\\"
        else:
            return

        output = []
        for file in os.listdir(path):
            if '_' + run_id + '-' in file:
                with open(path + '\\' + file, 'rb') as f:
                    while True:
                        try:
                            output.append(pickle.load(f))
                        except EOFError:
                            break
        return output 

    @staticmethod
    def delete_output(run_id):
        home = expanduser('~')
        if os.path.exists(home + "\\.observatory"):
            path = home + "\\.observatory\\outputs\\"
        else:
            return False

        for file in os.listdir(path):
            if '_' + run_id + '-' in file:
                os.remove(path + file)
                return True
        
