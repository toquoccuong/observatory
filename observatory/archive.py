from os import path, listdir, makedirs
import json
import tempfile
import tarfile


def create(base_path, model, version, experiment, run_id):
    """
    Creates a new model archive

    Parameters
    ----------
    base_path : str
        Base folder where all models are stored
    model : str
        The name of the model
    version : int
        The version of the model
    experiment : str
        The experiment ID
    run_id : str
        The ID of the run

    Returns
    -------
    The path where the archive file is stored.
    """
    _, output_file = tempfile.mkstemp('.tar.gz')
    model_folder = path.join(base_path, model, str(version), experiment, run_id)

    if not path.exists(model_folder):
        raise AssertionError('Specified model data could not be found. Make sure you refer ' +
                             'to a valid model, version, experiment and run identifier.')

    metadata = {
        'model': model,
        'version': version,
        'experiment': experiment,
        'run_id': run_id
    }

    # Store the metadata on disk, we know this is valid since the folder exists :-)
    with open(path.join(model_folder, 'metadata.json'), 'w') as metadata_file:
        json.dump(metadata, metadata_file)

    # Create the actual archive file.
    # This includes all files from the specified model folder
    with tarfile.open(output_file, 'w:gz') as archive_file:
        for item in listdir(model_folder):
            archive_file.add(path.join(model_folder, item), item, recursive=True)

    return output_file


def extract(filename, output_path):
    """
    Extracts a model archive on disk

    Parameters
    ----------
    filename : str
        The filename of the model archive to extract
    output_path : str
        The path to the folder to extract the model
    """

    makedirs(output_path, exist_ok=True)

    with tarfile.open(filename, 'r:gz') as archive_file:
        archive_file.extractall(output_path)
