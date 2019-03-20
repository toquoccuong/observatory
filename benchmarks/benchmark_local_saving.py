import json
import pickle
import _pickle as cPickle
import sqlite3
from tables import *
import numpy
from datetime import datetime
import pdb
from uuid import uuid4
#import benchmarks.sqlite_database_creation_script
#import benchmarks.pytables_database_creation_script
filepath = 'C:\\Users\\MichielL\\Documents\\observatory_output\\'
startdate = None

class benchmark_text:

    def record_session_start(self, model, version, experiment, run_id):

        file = open(filepath +'txt_files\\benchmark_text_observatory_run_' + str(run_id) + '.txt','a')
        file.write('\nModel: ' + model)
        file.write('\nVersion: ' + str(version))
        file.write('\nExperiment: ' + experiment)
        file.write('\nRun: ' + run_id)
        file.write('\n' + 'Run started at: ' + str(datetime.now()))
        file.close()

    def record_session_end(self, model, version, experiment, run_id, status):
        file = open(filepath +'txt_files\\benchmark_text_observatory_run_' + str(run_id) + '.txt','a')
        file.write('\n' + 'Run ended at: ' + str(datetime.now()))
        file.close()

    def record_metric(self, model, version, experiment, run_id, name, value):
        """
        This function serves to benchmark the time is takes to save files to disk, using file saving
        """
        data = [name, value]
        datastr = str(data).strip('[]')
        file = open(filepath +'txt_files\\benchmark_text_observatory_run_' + str(run_id) + '.txt','a')
        file.write('\n' + datastr) 
        file.close()

class benchmark_JSON:

    def record_session_start(self, model, version, experiment, run_id):
        data = [model, version, experiment, run_id, 'Started at:' + str(datetime.now())]
        with open(filepath + 'json_files\\benchmark_JSON_run_' + str(run_id) + '.json',  'a') as outfile:
            json.dump(data, outfile)

            outfile.write('\n')

    def record_session_end(self, model, version, experiment, run_id, status):
        data = [status, 'Ended at:' + str(datetime.now())]
        with open(filepath + 'json_files\\benchmark_JSON_run_' + str(run_id) + '.json',  'a') as outfile:
            json.dump(data, outfile)
            outfile.write('\n')

    def record_metric(self, model, version, experiment, run_id, name, value):   
        """
        This function serves to benchmark the time is takes to save files to disk, using JSON
        """
        data = [name, value]
        with open(filepath + 'json_files\\benchmark_JSON_run_' + str(run_id) + '.json', 'a') as outfile:
            json.dump(data, outfile)
            outfile.write('\n')

class benchmark_pickle:
    def record_session_start(self, model, version, experiment, run_id):
        data = [model, version, experiment, run_id, 'Started at:' + str(datetime.now())]
        file_name = filepath + 'pickle_files\\benchmark_pickle_run_' + str(run_id) + '.pkl'
        with open(file_name, 'ab') as fileObject:
            pickle.dump(data, fileObject, protocol= -1)

    def record_session_end(self, model, version, experiment, run_id, status):
        data = [status, 'Ended at:' + str(datetime.now())]
        file_name = filepath + 'pickle_files\\benchmark_pickle_run_' + str(run_id) + '.pkl'
        with open(file_name, 'ab') as fileObject:
            pickle.dump(data, fileObject, protocol= -1)
    
    def record_metric(self, model, version, experiment, run_id, name, value):
        """
        This function serves to benchmark the time is takes to save files to disk, using pickle
        """
        metric = [str(name), str(value)]
        file_name = filepath + 'cpickle_files\\benchmark_pickle_run_' + str(run_id) + '.pkl'
        with open(file_name, 'ab') as fileObject:
            pickle.dump(metric, fileObject, protocol= -1)
            
class benchmark_cpickle:
    def record_session_start(self, model, version, experiment, run_id):
        data = [model, version, experiment, run_id, 'Started at:' + str(datetime.now())]
        file_name = filepath + 'pickle_files\\benchmark_cpickle_run_' + str(run_id) + '.pkl'
        with open(file_name, 'ab') as fileObject:
            pickle.dump(data, fileObject, protocol= -1)

    def record_session_end(self, model, version, experiment, run_id, status):
        data = [status, 'Ended at:' + str(datetime.now())]
        file_name = filepath + 'cpickle_files\\benchmark_cpickle_run_' + str(run_id) + '.pkl'
        with open(file_name, 'ab') as fileObject:
            pickle.dump(data, fileObject, protocol= -1)
    
    def record_metric(self, model, version, experiment, run_id, name, value):
        """
        This function serves to benchmark the time is takes to save files to disk, using pickle
        """
        metric = [str(name), str(value)]
        file_name = filepath + 'cpickle_files\\benchmark_cpickle_run_' + str(run_id) + '.pkl'
        with open(file_name, 'ab') as fileObject:
            cPickle.dump(metric, fileObject, protocol= -1)

class benchmark_sqlite:
       
    def record_session_start(self, model, version, experiment, run_id):
        conn = sqlite3.connect(filepath + 'benchmark_sqlite.sqlite')
        c = conn.cursor()
        # insert into Model
        _model = [model, datetime.now()]
        c.execute('REPLACE INTO Model VALUES (?,?);', _model)
        # insert into Version
        _versionID = str(uuid4())
        _version = [_versionID, version, datetime.now(), model]
        c.execute('INSERT INTO Version VALUES (?,?,?,?);', _version)
        # insert into Experiment
        _experimentID = str(uuid4())
        _experiment = [_experimentID, experiment, datetime.now(), version]
        c.execute('INSERT INTO Experiment VALUES (?,?,?,?);', _experiment)
        # insert into Run
        startdate = datetime.now()
        _run = [run_id, startdate, 'running', experiment]
        c.execute('INSERT INTO Run(id, startdate, status ,experiment) VALUES (?,?,?,?);', _run)
        # save the changes
        conn.commit()
        # close the connection
        conn.close()

    def record_session_end(self, model, version, experiment, run_id, status):
        conn = sqlite3.connect(filepath + 'benchmark_sqlite.sqlite')
        c = conn.cursor()
        # replace into Run
        _run = [datetime.now(), run_id]
        c.execute('UPDATE Run Set enddate=? where id =?', _run)
        # save the changes
        conn.commit()
        # close the connection
        conn.close()

    def record_metric(self, model, version, experiment, run_id, name, value):
        """
        This function serves to benchmark the time is takes to save files to disk, using sqlite3
        """
        conn = sqlite3.connect(filepath+ 'benchmark_sqlite.sqlite')
        c = conn.cursor()
        # insert into Metric
        _metricID = str(uuid4())
        _metric = [_metricID, name, datetime.now(), value, run_id]
        c.execute('INSERT INTO Metric VALUES (?,?,?,?,?);', _metric)
        # save the changes
        conn.commit()
        # close the connection
        conn.close()

class benchmark_pytables: 

    def record_session_start(self, model, version, experiment, run_id):
        h5file = open_file(filepath + 'benchmark_pytables.h5', mode='a', title='Test File')

        model_table = h5file.root.observatory.model
        model_row = model_table.row
        _modelID = str(uuid4())
        model_row['id']     =  _modelID
        model_row['model']  =  model
        model_row['date']   =  datetime.now()
        model_row.append()
        model_table.flush()

        version_table = h5file.root.observatory.version
        version_row = version_table.row
        _versionID = str(uuid4())
        version_row['id']           = _versionID
        version_row['versionnmr']   = version
        version_row['date']         = datetime.now()
        version_row['model']        = model
        version_row.append()
        version_table.flush()

        experiment_table = h5file.root.observatory.experiment
        experiment_row = experiment_table.row
        _exID = str(uuid4())
        experiment_row['id']        = _exID
        experiment_row['name']      = experiment
        experiment_row['date']      = datetime.now()
        experiment_row['version']   = version
        experiment_row.append()
        experiment_table.flush()

        run_table = h5file.root.observatory.run
        run_row = run_table.row
        startdate = datetime.now()
        run_row['id']               = run_id
        run_row['startdate']        = startdate
        run_row['enddate']          = None
        run_row['status']           = 'running'
        run_row['experiment']       = experiment
        run_row.append()
        run_table.flush()

        h5file.close()

    def record_session_end(self, model, version, experiment, run_id, status):
        h5file = open_file(filepath +'benchmark_pytables.h5', mode='a', title='Test File')
        
        run_table = h5file.root.observatory.run
        run = run_table.row
        run['id']           = run_id
        run['startdate']    = startdate
        run['enddate']      = datetime.now()
        run['status']       = status
        run['experiment']   = experiment
        run.append()
        run_table.flush()

        h5file.close()
        
    def record_metric(self, model, version, experiment, run_id, name, value):
        """
        This function serves to benchmark the time is takes to save files to disk, using pytables
        """
        h5file = open_file(filepath +'benchmark_pytables.h5', mode='a', title='Test File')
        
        metric_table = h5file.root.observatory.metric
        metric = metric_table.row
        _metricID = str(uuid4())
        metric['id']        = _metricID
        metric['name']      = name
        metric['date']      = datetime.now()
        metric['value']     = value
        metric['run']       = run_id
        metric.append()
        metric_table.flush()

        h5file.close()
