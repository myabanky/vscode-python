# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import os

from pytest import Config, MonkeyPatch, Session

from .expected_discovery_test_output import (
    double_nested_folder_expected_output,
    dual_level_nested_folder_expected_output,
    empty_discovery_pytest_expected_output,
    simple_discovery_pytest_expected_output,
    unit_pytest_same_file_discovery_expected_output,
    unittest_folder_discovery_expected_output,
)
from .helpers import TEST_DATA_PATH, runner


def test_error_collect():
    """Test class for the error_discovery test. Runs pytest discovery on "error_discovery.py".

    Should return
    """
    actual = runner(
        ["--collect-only", os.fspath(TEST_DATA_PATH / "error_discovery.py")]
    )
    assert actual is not None
    assert actual.get("status") == "error"
    assert actual.get("cwd") == os.fspath(TEST_DATA_PATH)
    assert len(actual.get("errors", [])) == 1


def test_empty_collect():
    """Test class for the empty_discovery test. Runs pytest discovery on "empty_discovery.py".

    Should return success and an empty test tree.
    """
    actual = runner(
        ["--collect-only", os.fspath(TEST_DATA_PATH / "empty_discovery.py")]
    )
    assert actual is not None
    assert actual.get("status") == "success"
    assert actual.get("cwd") == os.fspath(TEST_DATA_PATH)
    assert actual.get("tests") == empty_discovery_pytest_expected_output


def test_simple_collect():
    actual = runner(["--collect-only", os.fspath(TEST_DATA_PATH / "simple_pytest.py")])
    # append to a file named "test.txt"
    assert actual is not None
    assert actual.get("tests") == simple_discovery_pytest_expected_output


def test_unit_pytest_collect():
    actual = runner(
        [
            "--collect-only",
            os.fspath(TEST_DATA_PATH / "unittest_pytest_same_file.py"),
        ]
    )
    assert actual is not None
    assert actual.get("status") == "success"
    assert actual.get("cwd") == os.fspath(TEST_DATA_PATH)
    assert actual.get("tests") == unit_pytest_same_file_discovery_expected_output


# ATM this is going to fail because the ACTUAL CODE IS INCORRECT.
# the error is the Unittest class was put inside the file object TWIC, once for each test, instead of a single time
# seem to be missing the checking that I had to see if the Unittest class already existed before creating a new one
def test_unittest_folder_collect():
    actual = runner(
        [
            "--collect-only",
            os.fspath(TEST_DATA_PATH / "unittest_folder"),
        ]
    )
    assert actual is not None
    assert actual.get("status") == "success"
    assert actual.get("cwd") == os.fspath(TEST_DATA_PATH)
    # write to a file named "test.txt"
    with open("test.py", "w") as f:
        json.dump(actual.get("tests"), f)
    assert actual.get("tests") == unittest_folder_discovery_expected_output


def test_dual_level_nested_folder_collect():
    actual = runner(
        [
            "--collect-only",
            os.fspath(TEST_DATA_PATH / "dual_level_nested_folder"),
        ]
    )
    assert actual is not None
    assert actual.get("status") == "success"
    assert actual.get("cwd") == os.fspath(TEST_DATA_PATH)
    assert actual.get("tests") == dual_level_nested_folder_expected_output


def test_double_nested_folder_collect():
    actual = runner(
        [
            "--collect-only",
            os.fspath(TEST_DATA_PATH / "double_nested_folder"),
        ]
    )
    assert actual is not None
    assert actual.get("status") == "success"
    assert actual.get("cwd") == os.fspath(TEST_DATA_PATH)
    assert actual.get("tests") == double_nested_folder_expected_output


# test UUIDs
