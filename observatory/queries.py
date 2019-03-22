from os import path

from observatory import archive, settings

PAGE_SIZE = 20

es = None


class PagedResultSet:
    """
    The paged result set is used to communicate a set of search
    results returned by a search query.

    This class is used by the dashboard API to return search results
    to the javascript client.
    """

    def __init__(self, page_index, page_size, total_items, data):
        """
        Initializes a new instance of PagedResultSet

        Parameters
        ----------
        page_index : int
            The page index
        page_size : int
            The number of items on a page
        total_items : int
            The total number of items available
        data : list
            The list of records on the page
        """
        self.page_index = page_index
        self.page_size = page_size
        self.total_items = total_items
        self.data = data


def configure(seed_nodes):
    """
    Configures the query module to connect to a specific set of
    elastic search nodes.

    When the query module is configured, it will automatically
    discover other nodes in the cluster.
    Also, when the connection is lost, it will be automatically
    reestablished when the cluster becomes available again.

    Parameters
    ---------
    seed_nodes : [string]
        The list of seed nodes to connect to.
    """
    global es

    print('Queries module configured to connect to {}'.format(seed_nodes))


def find_items(type_name, query, page_index):
    """
    Executes a search query for the specified item type and retrieves
    the specified search results page.

    This function assumes you're looking model, version, experiment or run.
    The index name is derived from the type parameter, if it doesn't exist you
    will receive a HTTP error.

    Parameters
    ----------
    type_name : str
        The type of item to find
    query : object
        The query DSL object to use for executing the query
    page_index : int
        The page index to retrieve

    Returns
    -------
    dictionary
        The results, this will contain a list of max. 20 items.
    """
    global es

    return


def find_models(page_index=0):
    """
    Finds all stored models in the search index

    Parameters
    ----------
    page_index : int
        The page index to retrieve from the resultset

    Returns
    -------
    PagedResultSet
        The paged results for the search query
    """
    search_query = {
        'query': {
            'match_all': {}
        }
    }

    results = find_items('model', search_query, page_index)

    records = []
    total_items = results['hits']['total']

    # Elastic search always returns results,
    # even when you request a non-existing page.
    # To prevent weird behavior in our api,
    # we check for this and return empty results
    # when you requested an empty page.
    if total_items < page_index * PAGE_SIZE:
        return PagedResultSet(page_index, PAGE_SIZE, total_items, [])

    for model in results['hits']['hits']:
        records.append({
            'name': model['_id'],
            'date_created': model['_source']['date_created']
        })

    return PagedResultSet(page_index, PAGE_SIZE, total_items, records)


def find_versions(item, page_index=0):
    """
    Finds all versions of a specific model.

    Parameters
    ----------
    model : str
        The name of the model to retrieve the versions for
    page_index : int
        The page index to retrieve from the search results

    Returns
    -------
    PagedResultSet
        The paged results for the search query

    """
    search_query = {
        'query': {
            'term': {
                'model': item
            }
        }
    }

    results = find_items('version', search_query, page_index)

    records = []
    total_items = results['hits']['total']

    # Elastic search always returns results,
    # even when you request a non-existing page.
    # To prevent weird behavior in our api,
    # we check for this and return empty results
    # when you requested an empty page.
    if total_items < page_index * PAGE_SIZE:
        return PagedResultSet(page_index, PAGE_SIZE, total_items, [])

    for item in results['hits']['hits']:
        records.append({
            'model': item['_source']['model'],
            'version_number': item['_source']['version_number'],
            'date_created': item['_source']['date_created']
        })

    return PagedResultSet(page_index, PAGE_SIZE, total_items, records)


def find_experiments(model, version, page_index=0):
    """
    Finds all experiments of a specific model/version combination.

    Parameters
    ----------
    model : str
        The name of the model to retrieve the experiments for
    version : int
        The version of the model to retrieve the experiments for
    page_index : int
        The page index to retrieve from the search results

    Returns
    -------
    PagedResultSet
        The paged results for the search query

    """

    # We use filter queries instead of regular boolean queries.
    # This is done so that the sort order isn't influenced.
    # We may need to add additional sorting to make a sensible resultset.
    search_query = {
        'query': {
            'bool': {
                'filter': [
                    {'term': {'model': model}},
                    {'term': {'version': version}}
                ]
            }
        }
    }

    results = find_items('experiment', search_query, page_index)

    records = []
    total_items = results['hits']['total']

    # Elastic search always returns results,
    # even when you request a non-existing page.
    # To prevent weird behavior in our api,
    # we check for this and return empty results
    # when you requested an empty page.
    if total_items < page_index * PAGE_SIZE:
        return PagedResultSet(page_index, PAGE_SIZE, total_items, [])

    for item in results['hits']['hits']:
        records.append({
            'model': item['_source']['model'],
            'version': item['_source']['version'],
            'name': item['_source']['experiment'],
            'date_created': item['_source']['date_created']
        })

    return PagedResultSet(page_index, PAGE_SIZE, total_items, records)


def find_runs(model, version, experiment, page_index=0):
    """
        Finds all runs of a specific model/version/experiment combination.

        Parameters
        ----------
        model : str
            The name of the model to retrieve the experiments for
        version : int
            The version of the model to retrieve the experiments for
        experiment : str
            The experiment to find the runs for
        page_index : int
            The page index to retrieve from the search results

        Returns
        -------
        PagedResultSet
            The paged results for the search query

        """

    # We use filter queries instead of regular boolean queries.
    # This is done so that the sort order isn't influenced.
    # We may need to add additional sorting to make a sensible resultset.
    search_query = {
        'query': {
            'bool': {
                'filter': [
                    {'term': {'model': model}},
                    {'term': {'version': version}},
                    {'term': {'experiment': experiment}}
                ]
            }
        }
    }

    results = find_items('run', search_query, page_index)

    records = []
    total_items = results['hits']['total']

    # Elastic search always returns results,
    # even when you request a non-existing page.
    # To prevent weird behavior in our api,
    # we check for this and return empty results
    # when you requested an empty page.
    if total_items < page_index * PAGE_SIZE:
        return PagedResultSet(page_index, PAGE_SIZE, total_items, [])

    for item in results['hits']['hits']:
        records.append({
            'id': item['_id'],
            'model': item['_source']['model'],
            'version': item['_source']['version'],
            'experiment': item['_source']['experiment'],
            'date_created': item['_source']['date_created']
        })

    return PagedResultSet(page_index, PAGE_SIZE, total_items, records)


def model_data_available(model, version, experiment, run_id):
    """
    Determines whether there's model data available for download.
    It could be that there's metadata about the model, but no outputs
    or settings.

    Parameters:
    -----------
    model : str
        The name of the model
    version : int
        The version of the model
    experiment : str
        The name of the experiment
    run_id : str
        The ID of the run

    Returns:
    --------
    boolean
        This method returns True when there are outputs and/or settings
        available for download.
        Otherwise this method returns False.
    """
    model_path = path.join(settings.base_path, model, str(version),
                           experiment, run_id)
    return path.exists(model_path)
