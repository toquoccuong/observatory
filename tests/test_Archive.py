import os
import pickle
from os.path import expanduser

import pytest
import requests
from observatory.archive import Archive

@pytest.fixture(scope="session")
def test_file():
    os.remove(expanduser('~' + '\\.observatory\\metrics\\test_v1_test_test.pkl'))
    path = expanduser('~') + "\\.observatory\\metrics\\test_v1_test_12345678-017f-41ce-b4b7-735bf7123332.pkl"
    data = []
    data.append(['loss', 255])
    with open(path, 'wb') as f:
        pickle.dump(data, f)
    yield path

    os.remove(expanduser('~') + "\\.observatory\\metrics\\test_v1_test_12345678-017f-41ce-b4b7-735bf7123332.pkl")

def test_get_model(test_file):
    data = Archive.get_model(Archive, 'test', test_file[:-53])

    assert data == ['1']

def test_get_version(test_file):
    data = Archive.get_version(Archive, 'test', '1', test_file[:-53])

    assert data == ['test']

def test_get_experiment(test_file):
    data = Archive.get_experiment(Archive, 'test', '1', 'test', test_file[:-53])

    assert data == ['12345678']

def test_get_run(test_file):
    data = Archive.get_run('12345678', test_file[:-53])

    assert data == [[['loss', 255]]]