"""
This module can be used to download data from the observatory server.
Typically you first track your model data with :func:`start_run <observatory.tracking.start_run>`.

Once you have collected data you can download the model data using the :func:`download_model <observatory.serving.download>`
function. 

Please refer to the individual function specs for more information how to use these functions.
"""
from concurrent import futures
import grpc

import re
import tempfile
from observatory.protobuf import observatory_pb2, observatory_pb2_grpc
from observatory import settings
from observatory import archive
from observatory.constants import LABEL_PATTERN


def download_model(**kwargs):
    """
    Downloads a model from the server and stores it in a local folder.

    This method will download a tarball from the server and extract it in a folder specified with the path argument.
    The model folder will contain all outputs you stored for the model.

    Additionally a settings.json file is included, which contains the settings that you stored earlier.
    Finally, a metadata.json file is included, which contains all the necessary metadata for the model,
    the name, version, experiment ID and run ID.

    Parameters
    ----------
    model : str
        The name of the model
    version : int
        The version number of the model
    experiment : str, optional
        The name of the experiment
    run_id : str
        The ID of the run
    path : str, optional
        The path to store the model, defaults to the current working folder.

    Returns
    -------
    The path to the model folder. You can access all the files in this folder.
    """

    model = kwargs.get('model', None)
    version = kwargs.get('version', None)
    run_id = kwargs.get('run_id', None)
    experiment = kwargs.get('experiment', 'default')
    path = kwargs.get('path', '.')

    if model is None:
        raise AssertionError('Please provide a model to download')

    if version is None:
        raise AssertionError('Please provide a version to download')

    if run_id is None:
        raise AssertionError('Please provide the ID of the run to download')

    if version <= 0:
        raise AssertionError('Version must be greater than zero')

    if not re.match(LABEL_PATTERN, model):
        raise AssertionError('name is invalid. It can contain ' +
                             'lower-case alpha-numeric characters and dashes only.')

    if experiment != 'default' and not re.match(LABEL_PATTERN, model):
        raise AssertionError('experiment is invalid. It can contain ' +
                             'lower-case alpha-numeric characters and dashes only.')

    channel = grpc.insecure_channel(settings.server_url)
    model_stub = observatory_pb2_grpc.ModelServiceStub(channel)

    request = observatory_pb2.DownloadModelRequest(
        model=model,
        version=version,
        experiment=experiment,
        run_id=run_id)

    response_iterator = model_stub.DownloadModel(request)

    _, temp_filename = tempfile.mkstemp('.tar.gz')

    with open(temp_filename, 'wb') as archive_file:
        for chunk in response_iterator:
            archive_file.write(chunk.chunk)

    archive.extract(temp_filename, path)

