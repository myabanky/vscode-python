# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import os

import pytest
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


@pytest.mark.parametrize(
    "file, expected_error_num",
    [("error_parametrize_discovery.py", 1), ("error_syntax_discovery.py", 1)],
)
def test_error_collect(file, expected_error_num):
    """Test class for the error_discovery test. Runs pytest discovery on "error_discovery.py".

    Should return
    """
    actual = runner(["--collect-only", os.fspath(TEST_DATA_PATH / file)])
    assert actual is not None
    assert actual.get("status") == "error"
    assert actual.get("cwd") == os.fspath(TEST_DATA_PATH)
    assert len(actual.get("errors", [])) == expected_error_num


@pytest.mark.parametrize(
    "file, expected_const",
    [
        ("empty_discovery.py", empty_discovery_pytest_expected_output),
        ("simple_pytest.py", simple_discovery_pytest_expected_output),
        (
            "unittest_pytest_same_file.py",
            unit_pytest_same_file_discovery_expected_output,
        ),
        ("unittest_folder", unittest_folder_discovery_expected_output),
        ("dual_level_nested_folder", dual_level_nested_folder_expected_output),
        ("double_nested_folder", double_nested_folder_expected_output),
    ],
)
def test_pytest_collect(file, expected_const):
    actual = runner(
        [
            "--collect-only",
            os.fspath(TEST_DATA_PATH / file),
        ]
    )
    assert actual is not None
    assert actual.get("status") == "success"
    assert actual.get("cwd") == os.fspath(TEST_DATA_PATH)
    assert actual.get("tests") == expected_const


# test UUIDs
