# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import os

import pytest

from .expected_discovery_test_output import (
    doctest_pytest_expected_output,
    double_nested_folder_expected_output,
    dual_level_nested_folder_expected_output,
    empty_discovery_pytest_expected_output,
    parametrize_tests_expected_output,
    simple_discovery_pytest_expected_output,
    unit_pytest_same_file_discovery_expected_output,
    unittest_folder_discovery_expected_output,
)
from .helpers import TEST_DATA_PATH, runner


@pytest.mark.parametrize(
    "file, expected_error_num",
    [("error_parametrize_discovery.py", 1), ("error_syntax_discovery.txt", 1)],
)
def test_error_collect(file, expected_error_num):
    """
    Tests pytest discovery on specific files that are expected to return errors.
    The json should still be returned but the errors list should be present.
    """
    rename = False
    py_name = ""
    original_name = ""
    # Saving some files as .txt to avoid that file displaying an error and
    # just rename it before running this test in order to test the error handling.
    if file.endswith(".txt"):
        py_name = os.fspath(TEST_DATA_PATH / file[:-4]) + ".py"
        original_name = os.fspath(TEST_DATA_PATH / file)
        os.rename(original_name, py_name)
        file = py_name
        rename = True
    actual = runner(["--collect-only", os.fspath(TEST_DATA_PATH / file)])
    assert actual
    assert actual.get("status") == "error"
    assert actual.get("cwd") == os.fspath(TEST_DATA_PATH)
    assert len(actual.get("errors", [])) == expected_error_num
    if rename:
        os.rename(py_name, original_name)


# For the following tests, the expected output includes the line number that the test is on.
# Therefore if the test file is changed (lines are added or deleted), the expected output will need to be updated to match.
@pytest.mark.parametrize(
    "file, expected_const",
    [
        ("parametrize_tests.py", parametrize_tests_expected_output),
        ("empty_discovery.py", empty_discovery_pytest_expected_output),
        ("simple_pytest.py", simple_discovery_pytest_expected_output),
        (
            "unittest_pytest_same_file.py",
            unit_pytest_same_file_discovery_expected_output,
        ),
        ("unittest_folder", unittest_folder_discovery_expected_output),
        ("dual_level_nested_folder", dual_level_nested_folder_expected_output),
        ("double_nested_folder", double_nested_folder_expected_output),
        ("text_docstring.txt", doctest_pytest_expected_output),
    ],
)
def test_pytest_collect(file, expected_const):
    """
    Test to test pytest discovery on a variety of test files/ folder structures.
    Uses variables from expected_discovery_test_output.py to store the expected dictionary return.
    Only handles discovery and therefore already contains the arg --collect-only.
    All test discovery will succeed, be in the correct cwd, and match expected test output.
    """
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
