import json
import pickle
import _pickle as cPickle
import sqlite3
import tables
import numpy
from datetime import datetime
import pdb
from uuid import uuid4

class benchmark:

    
    
    def benchmark_text_record_metric(self, model, version, experiment, run_id, name, value):
        """
        This function serves to benchmark the time is takes to save files to disk, using file saving
        """
        filepath = 'benchmarks\outputs\\'
        data = [model, version, experiment, run_id, name, value]
        datastr = str(data).strip('[]')
        file = open(filepath +'benchmark_text.txt','a')
        file.write('\n' + datastr) 
        file.close()

    def benchmark_JSON_record_metric(self, model, version, experiment, run_id, name, value):   
        """
        This function serves to benchmark the time is takes to save files to disk, using JSON
        """
        filepath = 'benchmarks\outputs\\'
        data = [model, version, experiment, run_id, name, value]
        with open(filepath + 'benchmark_JSON.json', 'a') as outfile:
            json.dump(data, outfile)
            outfile.write('\n')

    def benchmark_pickle_record_metric(self, model, version, experiment, run_id, name, value):
        """
        This function serves to benchmark the time is takes to save files to disk, using pickle
        """
        filepath = 'benchmarks\outputs\\'
        metric = [str(model), str(version), str(experiment), str(run_id), str(name), str(value)]
        file_name = 'benchmark_pickle.txt'
        with open(file_name, 'ab') as fileObject:
            pickle.dump(metric, fileObject)
            

    def benchmark_cpickle_record_metric(self, model, version, experiment, run_id, name, value):
        """
        This function serves to benchmark the time is takes to save files to disk, using file cPickle
        """
        filepath = 'benchmarks\outputs\\'
        metric = [model, version, experiment, run_id, name, value]
        file_name = filepath+ 'benchmark_cPickle'
        with open(file_name,  'ab') as fileObject:
            cPickle.dump(metric, fileObject)
            
    def benchmark_sqlite_record_session_start(self, model, version, experiment, run_id):
        filepath = 'benchmarks\outputs\\'
        conn = sqlite3.connect(filepath+ 'benchmark_sqlite.sqlite')
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
        _run = [run_id, datetime.now(), 'running', experiment]
        c.execute('INSERT INTO Run(id, startdate, status ,experiment) VALUES (?,?,?,?);', _run)
        # save the changes
        conn.commit()
        # close the connection
        conn.close()

    def benchmark_sqlite_record_session_end(self, model, version, experiment, run_id, status):
        filepath = 'benchmarks\outputs\\'
        conn = sqlite3.connect(filepath+ 'benchmark_sqlite.sqlite')
        c = conn.cursor()
        # replace into Run
        _run = [run_id, datetime.now(), status]
        c.execute('REPLACE INTO Run (id, enddate, status) VALUES (?,?,?);', _run)
        # save the changes
        conn.commit()
        # close the connection
        conn.close()

    def benchmark_sqlite_record_metric(self, model, version, experiment, run_id, name, value):
        """
        This function serves to benchmark the time is takes to save files to disk, using sqlite3
        """
        #
        # Needs some work, allways getting UNIQUE contraints. this is because the same record gets inserted 23 (in this case)
        # Need to find a way to only insert Model, Version, Experiment, Run once
        # Then insert Metric as many times as needed.
        #

        filepath = 'benchmarks\outputs\\'
        #metric = [model, version, experiment, run_id, name, value]
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

    def benchmark_pytables_record_metric(self, model, version, experiment, run_id, name, value):
        """
        This function serves to benchmark the time is takes to save files to disk, using pytables
        """
        filepath = 'benchmarks\outputs\\'
        h5file = tables.open_file(filepath +'benchmark_pytables.h5', mode='ab', title='Test File')
        group = h5file.create_group('/',  'Metric', 'Metric Information')
        table = h5file.create_table(group, 'readout', Metric, 'readout example')
        metric = table.row
        metric['model'] = model
        metric['version'] = version
        metric['experimentl'] = experiment
        metric['run_id'] = run_id
        metric['name'] = name
        metric['value'] = value

        # Insert a new metric record
        metric.append()
        table.flush()

class Metric(tables.IsDescription):
    model 		= tables.StringCol(16)
    version	 	= tables.Int32Col()
    experiment	= tables.StringCol(16)
    run_id		= tables.StringCol(16)
    timestamp	= tables.StringCol(16)
    metric 		= tables.StringCol(16)
    value		= tables.Float32Col()

