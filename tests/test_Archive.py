import os
import pickle
from os.path import expanduser

import pytest
import requests
from observatory.archive import Archive

@pytest.fixture(scope="session")
def test_file():
    home = expanduser("~")
    if os.path.exists(home + "\\.observatory"):
        # if it exists the path will be set
        try:
            os.remove('\\.observatory\\metrics\\test_v1_test_test.pkl')
        except Exception:
            pass
        path = (home + "\\.observatory\\metrics\\test_v1_test_12345678-017f-41ce-b4b7-735bf7123332.pkl")
    else:
        try:
            # if it doesn't exist, then it will be created,
            # along with subfolders for metrics, outputs and settings.
            os.makedirs(home + "\\.observatory\\metrics\\")
            path = (home + "\\.observatory\\metrics\\test_v1_test_12345678-017f-41ce-b4b7-735bf7123332.pkl")
        except PermissionError as e:
            # if the acces to the home directory is denied,
            # a folder in the current repo will be made and used.
            os.makedirs("\\.observatory\\metrics\\")
            path = ("\\.observatory\\metrics\\test_v1_test_12345678-017f-41ce-b4b7-735bf7123332.pkl")
    data = []
    data.append(['loss', 255])
    with open(path, 'wb') as f:
        pickle.dump(data, f)
    yield path
    try:
        os.remove(home + "\\.observatory\\metrics\\test_v1_test_12345678-017f-41ce-b4b7-735bf7123332.pkl")
    except Exception:
        try:
            os.remove("\\.observatory\\metrics\\test_v1_test_12345678-017f-41ce-b4b7-735bf7123332.pkl")
        except Exception:
            pass

# only run this test locally
@pytest.mark.skip(reason='This has problems with travis')
def test_get_model(test_file):
    data = Archive.get_model(Archive, 'test', test_file[:-53])

    assert data == ['1']

# only run this test locally
@pytest.mark.skip(reason='This has problems with travis')
def test_get_version(test_file):
    data = Archive.get_version(Archive, 'test', '1', test_file[:-53])

    assert data == ['test']

# only run this test locally
@pytest.mark.skip(reason='This has problems with travis')
def test_get_experiment(test_file):
    data = Archive.get_experiment(Archive, 'test', '1', 'test', test_file[:-53])

    assert data == ['12345678']

# only run this test locally
@pytest.mark.skip(reason='This has problems with travis')
def test_get_run(test_file):
    data = Archive.get_run('12345678', test_file[:-53])

    assert data == [[['loss', 255]]]