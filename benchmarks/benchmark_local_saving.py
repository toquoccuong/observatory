import json
import pickle
import _pickle as cPickle
import sqlite3
from tables import *
import numpy
from datetime import datetime
import pdb
from uuid import uuid4
import benchmarks.sqlite_database_creation_script
import benchmarks.pytables_database_creation_script
filepath = 'benchmarks\outputs\\'
startdate = None

class benchmark_text:
    def record_metric(self, model, version, experiment, run_id, name, value):
        """
        This function serves to benchmark the time is takes to save files to disk, using file saving
        """
        data = [model, version, experiment, run_id, name, value]
        datastr = str(data).strip('[]')
        file = open(filepath +'benchmark_text.txt','a')
        file.write('\n' + datastr) 
        file.close()

class benchmark_JSON:
    def record_metric(self, model, version, experiment, run_id, name, value):   
        """
        This function serves to benchmark the time is takes to save files to disk, using JSON
        """
        data = [model, version, experiment, run_id, name, value]
        with open(filepath + 'benchmark_JSON.json', 'a') as outfile:
            json.dump(data, outfile)
            outfile.write('\n')

class benchmark_pickle:
    def record_metric(self, model, version, experiment, run_id, name, value):
        """
        This function serves to benchmark the time is takes to save files to disk, using pickle
        """
        metric = [str(model), str(version), str(experiment), str(run_id), str(name), str(value)]
        file_name = 'benchmark_pickle.txt'
        with open(file_name, 'ab') as fileObject:
            pickle.dump(metric, fileObject)
            
class benchmark_cpickle:
    def record_metric(self, model, version, experiment, run_id, name, value):
        """
        This function serves to benchmark the time is takes to save files to disk, using file cPickle
        """
        metric = [model, version, experiment, run_id, name, value]
        file_name = filepath+ 'benchmark_cPickle'
        with open(file_name,  'ab') as fileObject:
            cPickle.dump(metric, fileObject)

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
        _run = [run_id, startdate, datetime.now(), status, experiment]
        c.execute('REPLACE INTO Run (id, startdate, enddate, status, experiment) VALUES (?,?,?,?,?);', _run)
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
        h5file = open_file('U:\Observatory\\benchmarks\outputs\\benchmark_pytables.h5', mode='a', title='Test File')

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
