import os
import pickle
from os.path import expanduser

import pytest
import requests
from observatory.serving import ServingClient

serving = ServingClient()

def test_validate_model_empty():
    with pytest.raises(AssertionError):
            serving.validate_model('')

def test_validate_model_uppercase():
    with pytest.raises(AssertionError):
            serving.validate_model('Testmodel')

def test_validate_version_empty():
        with pytest.raises(AssertionError):
                serving.validate_version('')

def test_validate_version_letter():
        with pytest.raises(AssertionError):
                serving.validate_version('v2')

def test_validate_experiment_empty():
        with pytest.raises(AssertionError):
                serving.validate_experiment('')  

def test_validate_experiment_uppercase():
        with pytest.raises(AssertionError):
                serving.validate_experiment('Experiment')  

def test_validate_run_length_too_long():
        with pytest.raises(AssertionError):
                serving.validate_run('123456789')

def test_validate_run_length_too_short():
        with pytest.raises(AssertionError):
                serving.validate_run('1234657')

def test_validate_run_empty():
        with pytest.raises(AssertionError):
                serving.validate_run('')

def test_validate_run_uppercase ():
        with pytest.raises(AssertionError):
                serving.validate_run('A134567')    