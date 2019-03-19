import json
from os import path, makedirs
import os
from os.path import expanduser
from observatory import settings
import pickle
from datetime import datetime
from pathlib import Path


class Sink():
    """
    This class handles all the saving of the data using Pickle.
    The Pickle protocol being used is the highest possible protocol (-1)
    """


    def __init__(self):
        self._path = None
        # this module depends on the .observatory directory. So we need to make sure it exists.
        home = expanduser("~")
        if os.path.exists(home + "\\.observatory"):
            # if it exists the path will be set
            self._path = (home + "\\.observatory\\")
        else:
            try:
                # if it doesn't exist, then it will be created, along with subfolders for metrics, outputs and settings.
                os.makedirs(home + "\\.observatory")
                os.makedirs(home + "\\.observatory\\metrics")
                os.makedirs(home + "\\.observatory\\outputs")
                os.makedirs(home + "\\.observatory\\settings")
                self._path = (home + "\\.observatory\\")
            except Exception as e:
                self._path = expanduser('~')
                print (e)
                pass
        
    def record_metric(self, model, run_id, metric_name, metric_value):
        """
        Records a metric value.

        This method records a single metric value for a run. All metrics belonging to one run will
        be saved in the same file. So for every run a new file will be created.

        Parameters
        ----------
        run_id : string
            The ID of the run
        timestamp : long
            The timestamp for the metric value
        metric_name : string
            The name of the metric
        metric_value : float
            The value of the metric
        """
        metric = [metric_name, metric_value]
        try:
            file_name = self._path + "metrics\\" + str(model)+ '_' + str(run_id) + '.pkl'
            with open(file_name, 'ab') as fileObject:
                pickle.dump(metric, fileObject, protocol= -1)
        except TypeError as e:
            # ! This gets thrown when _path is not set correctly, thus when sink is not initialized,
            # ! which under normal circumstances will not happen.
            # ? might need better error handeling, or might not be necessary at all.
            print (e)
        except PermissionError as e:
            # ! The PermissionError catch is in place so that Travis.ci doesnt fail the tests, 
            # ! because it is not allowed to save files in the travis home directory.
            # ! when using Observatory normally this should never occur.
            # ? might need beter error handleing.

            print (e)
            
        


    def record_session_start(self, model, version, experiment, run_id):
        """
        Records the start of a session

        When you start a new run, this method gets called to record the start of the session.
        After you've started a session you can record its final status and completion time with record_session_end.

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
        timestamp : int
            The timestamp
        """
        data = [model, version, experiment, run_id, datetime.now()]
        try:
            file_name = self._path + "metrics\\" + str(model)+ '_' + str(run_id) + '.pkl'
            with open(file_name, 'ab') as fileObject:
                    pickle.dump(data, fileObject, protocol= -1)
        except TypeError as e:
            print (e)
        except PermissionError as e:
            print (e)

    def record_session_end(self, model, run_id, status):
        """
        Records the end of a tracking session

        When you've started tracking a run with record_session_start you can call this method to signal
        the completion of the run. This updates the existing run document with the completion time
        and status of the run.

        Please note that this function raises an error when you try to complete a run that wasn't started earlier.
        This is done to prevent the tool from recording "empty" sessions.

        Parameters
        ----------
        status : str
            The status of the run (completed, failed)
        """
        data = [status, datetime.now()]
        try:
            file_name = self._path + "metrics\\" + str(model)+ '_' + str(run_id) + '.pkl'
            with open(file_name, 'ab') as fileObject:
                pickle.dump(data, fileObject, protocol= -1)
        except TypeError as e:
            print (e)
        except PermissionError as e:
            print (e)
            

    def record_settings(self, model, version, experiment, run_id, settings):
        """
        Records the settings used for a particular experiment run.

        When you record settings, you have to record all settings at once. There is
        no automatic merging of settings by this method.

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
        try:
            filename = self._path + "settings\\" + str(model) + '_' + str(run_id) + '_settings.pkl'
            with open(filename, 'ab') as f:
                pickle.dump(data, f, protocol=-1)
        except TypeError as e:
            print (e)
        except PermissionError as e:
            print (e)
            

    def record_output(self, model, version, experiment, run_id, filename, file):
        """
        Records the output for an experiment

        The output file is stored as part of the run. It is stored as-is without 
        any checks on the extension or file contents. 

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
        file : object
            The file handle
        """

        try:
            filename = self._path + "outputs\\" + str(model) + '_' + str(run_id) + '_output.pkl'
        except TypeError as e:
            print (e)
        except PermissionError as e:
            print (e)
            