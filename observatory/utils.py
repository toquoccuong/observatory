from elasticsearch import Elasticsearch


def index_name(name):
    """
    Translates a relative index name to a fully qualified index name by prepending 'observatory-'

    This method ensures that we don't overwrite search indices on a shared elastic search server.
    You should always refer to this method to correctly locate an index when writing or reading data
    from elastic search indices.

    Parameters
    ----------
    name : str
        Relative name of the index

    Returns
    -------
    str
        The fully qualified index name
    """
    if name is None:
        raise AssertionError('Must provide a name for the index')

    return 'observatory-{}'.format(name)


def es_client(seed_nodes):
    """
    Connects to an elastic search cluster on the specified nodes.

    Use this method whenever you need to connect to a search cluster.
    The client configured here will automatically reconnect when the connection is lost.

    Usage example:

    >>> es_client(['localhost'])

    Will return a configured client that connects to one node, localhost.
    Alternatively you can configure multiple nodes as a failover.

    >>> es_client(['server1', 'server2'])

    Please note that the initial nodes will be used as seed nodes. The client automatically
    discovers other nodes in the cluster and will use those when the seed nodes are no longer available.

    Parameters
    ----------
    seed_nodes : list
        A list of nodes for example `['localhost']`

    Returns
    -------
    object
        The configured elastic search client
    """

    if seed_nodes == [] or seed_nodes is None:
        client = Elasticsearch(
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            sniffer_timeout=60)
    else:
        client = Elasticsearch(
            seed_nodes,
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            sniffer_timeout=60)

    return client