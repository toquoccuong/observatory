import os
import pickle
from os.path import expanduser

import pytest
import requests

@pytest.fixture()
def test_file():
    path = expanduser('~') + "\\.observatory\\metrics\\test_v1_test_12345678-255.pkl"
    data = []
    for x in range(100):
        data.append(['loss', x])
    with open(path, 'wb') as f:
        pickle.dump(data, f)
    yield path

    os.remove(expanduser('~') + "\\.observatory\\metrics\\test_v1_test_12345678-255.pkl")

def test_get_model():
    pass

def test_get_version():
    pass

def test_get_experiment():
    pass

def test_get_run():
    pass