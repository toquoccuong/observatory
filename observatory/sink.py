import json
from os import path, makedirs
import os
from os.path import expanduser
import pickle
from datetime import datetime
from pathlib import Path


class Sink():
    """
    This class handles all the saving of the data using Pickle.
    The Pickle protocol being used is the highest possible protocol (-1)
    """

    def __init__(self):
        # this module depends on the .observatory directory.
        # So we need to make sure it exists.
        home = expanduser("~")
        if os.path.exists(home + "\\.observatory"):
            # if it exists the path will be set
            self._path = (home + "\\.observatory\\")
        else:
            try:
                # if it doesn't exist, then it will be created,
                # along with subfolders for metrics, outputs and settings.
                os.makedirs(home + "\\.observatory")
                os.makedirs(home + "\\.observatory\\metrics")
                os.makedirs(home + "\\.observatory\\outputs")
                os.makedirs(home + "\\.observatory\\settings")
                self._path = (home + "\\.observatory\\")
            except PermissionError as e:
                # if the acces to the home directory is denied,
                # a folder in the current repo will be made and used.
                os.makedirs("\\.observatory")
                self._path = ("\\.observatory\\")
                pass

    def write_data_to_filestream(self, file_stream, data):
        """
        This methods pickles all data, and writes is to the fileStream

        This method is separate to guarantee code testability
        """
        pickle.dump(data, file_stream, -1)

    def record_metric(self, model, version, experiment, run_id, metric_name, metric_value):
        """
        Records a metric value.

        This method records a single metric value for a run.
        All metrics belonging to one run will be saved in the same file.
        So for every run a new file will be created.

        Parameters
        ----------
        model : string
            The name of the model
        version : int
            The version number of the model
        experiment : string
            The name of the experiment
        run_id : string
            The ID of the run
        metric_name : string
            The name of the metric
        metric_value : float
            The value of the metric
        """
        metric = [metric_name, metric_value]

        file_name = self._path + "metrics\\" + model + '_v' + str(version) + '_' + experiment + '_' + run_id + '.pkl'
        with open(file_name, 'ab') as fileObject:
            self.write_data_to_filestream(fileObject, metric)

    def record_session_start(self, model, version, experiment, run_id):
        """
        Records the start of a session

        When you start a new run, this method gets called to record
        the start of the session.
        After you've started a session you can record its final status
        and completion time with record_session_end.

        Parameters
        ----------
        model : string
            The name of the model
        version : int
            The version number of the model
        experiment : string
            The name of the experiment
        run_id : string
            The ID of the run
        """
        data = [model, version, experiment, run_id, datetime.now()]

        file_name = self._path + "metrics\\" + model + '_v' + str(version) + '_' + experiment + '_' + run_id + '.pkl'
        with open(file_name, 'ab') as fileObject:
                self.write_data_to_filestream(fileObject, data)

    def record_session_end(self, model, version, experiment, run_id, status):
        """
        Records the end of a tracking session

        When you've started tracking a run with record_session_start you
        can call this method to signal
        the completion of the run. This updates the existing run document.
        with the completion time
        and status of the run.

        Please note that this function raises an error when you try to
        complete a run that wasn't started earlier.
        This is done to prevent the tool from recording "empty" sessions.

        Parameters
        ----------
        model : string
            The name of the model
        version : int
            The model version
        experiment : str
            The name of the experiment
        run_id : string
            The ID of the run
        status : str
            The status of the run (completed, failed)
        """
        data = [status, datetime.now()]

        file_name = self._path + "metrics\\" + model + '_v' + str(version) + '_' + experiment + '_' + run_id + '.pkl'
        with open(file_name, 'ab') as fileObject:
            self.write_data_to_filestream(fileObject, data)

    def record_settings(self, model, version, experiment, run_id, settings):
        """
        Records the settings used for a particular experiment run.

        When you record settings, you have to record all settings at once.
        There is no automatic merging of settings by this method.

        Parameters:
        -----------
        model : str
            The name of the model
        version : int
            The model version
        experiment : str
            The name of the experiment
        run_id : str
            The identifier for the run
        settings : dict
            The settings to record on disk
        """
        data = [model, version, experiment, run_id, settings]

        filename = self._path + "settings\\" + model + '_v' + str(version) + '_' + experiment + '_' + run_id + '.pkl'
        with open(filename, 'ab') as f:
            self.write_data_to_filestream(f, data)

    def record_output(self, model, filename, filepath):
        """
        Records the output for an experiment

        The output file is stored as part of the run.
        It is stored as-is without any checks on the extension
        or file contents.

        Parameters:
        -----------
        model : str
            The name of the model
        version : int
            The model version
        experiment : str
            The name of the experiment
        run_id : str
            The identifier for the run
        filename : str
            The filename of the file
        filepath : object
            The file location
        """
        # ? why do we record output, when its just coppying the ouput file
        # ? to the Observatory directory
        # ? wouldn't is be better to just save the file path
        # ? in the record_session_start() method
        output_dir = path.join(self._path + 'outputs\\')
        file_path = path.join(output_dir + model)
        with open(filepath, 'r') as fr:
            outStr = fr.readlines()
            with open(file_path, 'w') as fw:
                fw.writelines(outStr)
