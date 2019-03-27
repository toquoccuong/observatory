from os import path, listdir, makedirs
import os
from os.path import expanduser
from fnmatch import fnmatch as match
import json
import tempfile
import tarfile


"""
This module is currently not working.
As the rework of Obsrevatory progresses this will be fixed.
"""

class Archive():

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
            self._path = (home + "\\.observatory\\")
            return self._path
        else:
            print("no home directory found")

    @staticmethod
    def get_run(self, run_id):
        pass

    @staticmethod
    def get_model(self, model, path):
        """
        Gets the requested model

        Does not have to be perfecht match
        
        Arguments:
            model {str} -- model name
            path {str} -- Path to file destination
        
        Returns:
            list -- list of all found models containing the input value,
                    This might be more than one model, depending on the input
        """

        models = []
        for file in os.listdir(path):
            if model in file:
                models.append(file)
        return models

    @staticmethod
    def get_version(self, model, version, path):
        """
        Gets the requested version

        version has to be perfecht match
        
        Arguments:
            model {str} -- model name
            version {str} -- version number
            path {str} -- Path to file destination
        
        Returns:
            list -- list of all found versions
                    This is always one version
        """
        versions = []
        print("i got to verions")
        for file in os.listdir(path):
            if model in file:
                if '_v' + version in file:
                    versions.append(file)
        return versions

    @staticmethod
    def get_experiment(self, model, version, experiment, path):
        """
        Gets the requested version

        version has to be perfecht match
        
        Arguments:
            model {str} -- model name
            version {str} -- version number
            path {str} -- Path to file destination
        
        Returns:
            list -- list of all found versions
                    This is always one version
        """
        experiments = []
        print("i got to experiments")
        for file in os.listdir(path):
            if model in file:
                if '_v' + version + '_' in file:
                    if '_' + experiment + '_' in file:
                        experiments.append(file)
        return experiments