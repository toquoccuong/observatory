from tables import *
import numpy
from uuid import uuid4
import datetime

import os
import shutil
os.remove('C:\\Users\\USER\\Documents\\observatory_output\\benchmark_pytables.h5')

class Model(IsDescription):
    id          = StringCol(40)
    model       = StringCol(40)
    date        = StringCol(40)

class Version(IsDescription):
    id          = StringCol(40)
    versionnmr  = Float64Col()
    date        = StringCol(40)
    model       = StringCol(40)

class Experiment(IsDescription):
    id          = StringCol(40)
    name        = StringCol(36)
    date	    = StringCol(36)
    version     = StringCol(40)

class Run(IsDescription):
    id          = StringCol(40)
    startdate   = StringCol(40)
    enddate     = StringCol(40)
    status      = StringCol(40)
    experiment  = StringCol(40)

class Metric(IsDescription):
    id          = StringCol(40)
    name        = StringCol(36)
    date	    = StringCol(36)
    value		= Float32Col()
    run         = StringCol(40)

class Setting(IsDescription):
    id          = StringCol(40)
    date	    = StringCol(36)
    run         = StringCol(40)

class Output(IsDescription):
    id          = StringCol(40)
    date	    = StringCol(36)
    run         = StringCol(40)

filepath = 'C:\\Users\\USER\\Documents\\observatory_output\\'

h5file = open_file("C:\\Users\\USER\\Documents\\observatory_output\\benchmark_pytables.h5", "a", title="benchmark_pytables")

observatory_group = h5file.create_group("/", 'observatory', 'Obsrevatory metadata information')
model_table = h5file.create_table(observatory_group, 'model', Model, "Model example")
model = model_table.row
idm = str(uuid4())
model['id']     =  idm
model['model']  =  "test model"
model['date']   =   datetime.datetime.now()
model.append()
model_table.flush()

version_table = h5file.create_table(observatory_group, 'version', Version, "Version example")
version = version_table.row
idv = str(uuid4())
version['id']           = idv
version['versionnmr']   = 1.2
version['date']         = datetime.datetime.now()
version['model']        = "test model"
version.append()
version_table.flush()

experiment_table = h5file.create_table(observatory_group, 'experiment', Experiment, "Experiment example")
experiment = experiment_table.row
ide = str(uuid4())
experiment['id']        = ide
experiment['name']      = "test experiment"
experiment['date']      = datetime.datetime.now()
experiment['version']   = idv
experiment.append()
experiment_table.flush()

run_table = h5file.create_table(observatory_group, 'run', Run, "Run example")
run = run_table.row
idr = str(uuid4())
run['id']   = idr
run['startdate'] = datetime.datetime.now()
run['enddate'] = datetime.datetime.now()
run['status'] = 'completed'
run['experiment'] = ide
run.append()
run_table.flush()

metric_table = h5file.create_table(observatory_group, 'metric', Metric, "Metric example")
metric = metric_table.row
idme = str(uuid4())
metric['id'] = idme
metric['name'] = 'accuracy'
metric['date'] =  datetime.datetime.now()
metric['value'] = 0.89
metric['run'] = idr
metric.append()
metric_table.flush()

setting_table = h5file.create_table(observatory_group, 'setting', Setting, "Setting example")
setting = setting_table.row
ids = str(uuid4())
setting['id'] = ids
setting['date'] = datetime.datetime.now
setting['run'] = idr
setting.append()
setting_table.flush()

output_table = h5file.create_table(observatory_group, 'output', Output, "Output example")
output = output_table.row
ido = str(uuid4())
output['id'] = ido
output['date'] = datetime.datetime.now
output['run'] = idr
output.append()
output_table.flush()

h5file.close()