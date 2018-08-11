from elasticsearch import Elasticsearch

es = None


def configure(seed_nodes):
    """
    Configures the tracking sink to connect to a specific set of seed nodes
    """
    global es

    if seed_nodes == [] or seed_nodes is None:
        es = Elasticsearch(
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            sniffer_timeout=60)
    else:
        es = Elasticsearch(
            seed_nodes,
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            sniffer_timeout=60)

    print('Tracking sink is configured to connect to {}'.format(seed_nodes))


def ensure_index(model):
    """
    Ensures that a metrics index is available for recording model data.

    This method creates a new index with the correct mapping if one doesn't exist.
    Otherwise it simply reuses the existing index.

    Parameters
    ----------
    name : string
        The name of the index
    """
    global es

    if not es.indices.exists('metrics-{}'.format(model)):
        index_settings = {
            'settings': {
                'number_of_shards': 3,
                'number_of_replicas': 2
            },
            'mappings': {
                'metric': {
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
            }
        }

        es.indices.create('metrics-{}'.format(model), body=index_settings)


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

    ensure_index(model)

    document = {
        'model': model,
        'version': version,
        'experiment': experiment,
        'run_id': run_id,
        'timestamp': timestamp,
        'metric': metric_name,
        'value': metric_value
    }

    es.index(index='metrics-{}'.format(model), doc_type='metric', body=document)
