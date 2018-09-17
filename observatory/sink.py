import json
from os import path, makedirs
from observatory.utils import index_name, es_client

es = None


def configure(seed_nodes):
    """
    Configures the tracking sink to connect to a specific set of seed nodes.

    When the sink is configured, it will automatically discover other nodes in the cluster.
    Also, when the connection is lost, it will be automatically reestablished when the cluster becomes available again.

    Please note that data is still lost when no connection is available to the elastic search cluster.

    Parameters
    ---------
    seed_nodes : [string]
        The list of seed nodes to connect to.
    """
    global es

    es = es_client(seed_nodes)

    print('Tracking sink is configured to connect to {}'.format(seed_nodes))


def ensure_index(name, mapping):
    """
    Ensures that the specified index exists with the correct mapping.

    If the index exists, nothing is done.
    When the index doesn't exist, it will be created with the provided mapping.

    Parameters
    ----------
    name : str
        Name of the index
    mapping: object
        The mapping for the elastic search index
    """

    global es

    if not es.indices.exists(index_name(name)):
        index_settings = {
            'settings': {
                'number_of_shards': 3,
                'number_of_replicas': 2
            },
            'mappings': {
                name: mapping
            }
        }

        es.indices.create(index_name(name), body=index_settings)


def ensure_metrics_index():
    """
    Ensures that a metrics index is available for recording model data.

    This method creates a new index with the correct mapping if one doesn't exist.
    Otherwise it simply reuses the existing index.
    """
    mapping = {
        'properties': {
            'model': {'type': 'text'},
            'version': {'type': 'integer'},
            'experiment': {'type': 'text'},
            'run_id': {'type': 'text'},
            'timestamp': {'type': 'date'},
            'metric': {'type': 'text'},
            'value': {'type': 'float'}
        }
    }

    ensure_index('metrics', mapping)


def ensure_version_index():
    """
    Ensures that a version index is available for recording version data.

    This method creates a new index with the correct mapping if one doesn't exist.
    Otherwise it simply reuses the existing index.
    """
    mapping = {
        'properties': {
            'model': {'type': 'text'},
            'version_number': {'type': 'text'},
            'date_created': {'type': 'date'}
        }
    }

    ensure_index('version', mapping)


def ensure_model_index():
    """
    Ensures that a model index is available for recording model data.

    This method creates a new index with the correct mapping if one doesn't exist.
    Otherwise it simply reuses the existing index.
    """
    mapping = {
        'properties': {
            'date_created': {'type': 'date'}
        }
    }

    ensure_index('model', mapping)


def ensure_experiment_index():
    """
    Ensures that an experiment index is available for recording experiment data.

    This method creates a new index with the correct mapping if one doesn't exist.
    Otherwise it simply reuses the existing index.
    """
    mapping = {
        'properties': {
            'model': {'type': 'text'},
            'version': {'type': 'text'},
            'name': {'type': 'text'},
            'date_created': {'type': 'date'}
        }
    }

    ensure_index('experiment', mapping)


def ensure_run_index():
    """
    Ensures that a run index is available for recording run data.

    This method creates a new index with the correct mapping if one doesn't exist.
    Otherwise it simply reuses the existing index.
    """
    mapping = {
        'properties': {
            'started': {'type': 'date'},
            'completed': {'type': 'date'},
            'status': {'type': 'text'}
        }
    }

    ensure_index('run', mapping)


def record_metric(model, version, experiment, run_id, timestamp, metric_name, metric_value):
    """
    Records a metric value.

    This method records a single metric value for a run. If an index doesn't yet exist for the model, it will be
    created automatically with the correct mapping for recording model metadata.

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
    timestamp : long
        The timestamp for the metric value
    metric_name : string
        The name of the metric
    metric_value : float
        The value of the metric
    """
    global es

    ensure_metrics_index()

    document = {
        'model': model,
        'version': version,
        'experiment': experiment,
        'run_id': run_id,
        'timestamp': timestamp,
        'metric': metric_name,
        'value': metric_value
    }

    es.index(index='observatory-metrics', doc_type='metrics', body=document)


def ensure_model(model, timestamp):
    """
    Ensures that model metadata is recorded

    If the model does not exist, its metadata is recorded in the index.
    Otherwise, nothing is done.

    Parameters
    ----------
    model : str
        The name of the model
    timestamp : int
        The timestamp to use as creation date when the model doesn't exist.
    """
    global es

    ensure_model_index()

    if not es.exists(index=index_name('model'), doc_type='model', id=model):
        model_data = {
            'date_created': timestamp
        }

        es.index(index=index_name('model'), doc_type='model', id=model, body=model_data)


def ensure_version(model, version, timestamp):
    """
    Ensures that model metadata is recorded.

    If the version does not exist, its metadata is recorded in the index.
    Otherwise, nothing is done.

    Parameters
    ----------
    model : str
        The name of the model
    version : int
        The version number
    timestamp: int
        The timestamp to use for recording creation date of the version
    """
    global es

    ensure_version_index()

    identifier = '{}-{}'.format(model, version)

    if not es.exists(index=index_name('version'), doc_type='version', id=identifier):
        version_data = {
            'model': model,
            'version_number': version,
            'date_created': timestamp
        }

        es.index(index=index_name('version'), doc_type='version', id=identifier, body=version_data)


def ensure_experiment(model, version, experiment, timestamp):
    """
    Ensures that model metadata is recorded

    If the experiment does not exist, its metadata is recorded in the index.
    Otherwise, nothing is done.

    Parameters
    ----------
    model : str
        The name of the model
    version : int
        The version number
    experiment : str
        The name of the experiment
    timestamp : int
        Timestamp to use for the creation date of the experiment if it doesn't exist
    """
    global es

    ensure_experiment_index()

    identifier = '{}-{}-{}'.format(model, version, experiment)

    if not es.exists(index=index_name('experiment'), doc_type='experiment', id=identifier):
        experiment_data = {
            'model': model,
            'version': version,
            'experiment': experiment,
            'date_created': timestamp
        }

        es.index(index=index_name('experiment'), doc_type='experiment', id=identifier, body=experiment_data)


def record_session_start(model, version, experiment, run_id, timestamp):
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
    global es

    ensure_model(model, timestamp)
    ensure_version(model, version, timestamp)
    ensure_experiment(model, version, experiment, timestamp)

    identifier = '{}-{}-{}-{}'.format(model, version, experiment, run_id)

    if not es.exists(index=index_name('run'), doc_type='run', id=identifier):
        run_data = {
            'model': model,
            'version': version,
            'run_id': run_id
        }

        es.index(index=index_name('run'), doc_type='run', id=identifier, body=run_data)


def record_session_end(model, version, experiment, run_id, status, timestamp):
    """
    Records the end of a tracking session

    When you've started tracking a run with record_session_start you can call this method to signal
    the completion of the run. This updates the existing run document in the index with the completion time
    and status of the run.

    Please note that this function raises an error when you try to complete a run that wasn't started earlier.
    This is done to prevent the tool from recording "empty" sessions.

    Parameters
    ----------
    model : str
        The name of the model
    version : int
        The version number
    experiment : str
        The name of the experiment
    run_id : str
        The ID of the run
    status : str
        The status of the run (completed, failed)
    timestamp : int
        Timestamp indicating when the session was finished
    """
    global es

    ensure_model(model, timestamp)
    ensure_version(model, version, timestamp)
    ensure_experiment(model, version, experiment, timestamp)

    identifier = '{}-{}-{}-{}'.format(model, version, experiment, run_id)

    if not es.exists(index=index_name('run'), doc_type='run', id=identifier):
        raise AssertionError('There was no tracking session start recorded so a session end cannot be stored.')
    else:
        run_data = es.get(index=index_name('run'), doc_type='run', id=identifier)['_source']
        run_data['completed'] = timestamp
        run_data['status'] = status

        es.index(index='observatory-meta', doc_type='run', id=identifier, body=run_data)


def record_settings(model, version, experiment, run_id, settings):
    """
    Records the settings used for a particular experiment run.

    The settings are recorded in a settings.json file. 
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
    settings_directory = path.join(model, str(version), experiment, run_id)
    
    makedirs(settings_directory, exist_ok=True)

    with open(path.join(settings_directory, 'settings.json'), 'w') as settings_file:
        json.dump(settings, settings_file)


def record_output(model, version, experiment, run_id, filename, file):
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

    output_dir = path.join(model, str(version), experiment, run_id)
    file_path = path.join(output_dir, filename)

    makedirs(output_dir, exist_ok=True)

    file.save(file_path)
