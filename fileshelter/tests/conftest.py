from pytest import fixture

import os
import sys
import shutil
from uuid import uuid4

@fixture(scope="session")
def global_tests_dir():
    dir_path = os.path.abspath("./.test-tmp-{}".format(uuid4()))
    os.makedirs(dir_path)
    yield dir_path
    shutil.rmtree(dir_path)

@fixture
def test_dir(global_tests_dir):
    dir_path = os.path.join(global_tests_dir, "test-{}".format(uuid4()))
    os.makedirs(dir_path)
    yield dir_path
    shutil.rmtree(dir_path)