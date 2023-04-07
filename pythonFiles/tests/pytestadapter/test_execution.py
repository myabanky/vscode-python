# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import os
import shutil
import signal

import pytest

from . import expected_discovery_test_output
from .helpers import TEST_DATA_PATH, runner


def test_parameterized_error_collect():
    """Tests pytest discovery on specific file that incorrectly uses parametrize.

    The json should still be returned but the errors list should be present.
    """
    file_path_str = "error_parametrize_discovery.py"
    args = ['--port', '51927', '--uuid', '355c34de-c700-430b-b...eaac0cc91c', '--testids', 'test_u.TestInc.test_...ive_number', '--udiscovery', '-v', '-s', '.', '-p', 'test_*.py']
    actual = runner([file_path_str])
    assert actual
    assert all(item in actual for item in ("status", "cwd", "errors"))
    assert actual["status"] == "error"
    assert actual["cwd"] == os.fspath(TEST_DATA_PATH)
    assert len(actual["errors"]) == 2