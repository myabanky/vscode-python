# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

from pytest import Config, MonkeyPatch, Session

from .expected_test_output import (
    empty_discovery_pytest_expected_output,
    simple_discovery_pytest_expected_output,
    unit_pytest_discovery_pytest_expected_output,
)
from .helpers import TEST_DATA_PATH, runner

# def test_simple_collect():
#     result = runner(["--collect-only", os.fspath(TEST_DATA_PATH / "simple_discovery_pytest.py")])
#     assert result is not None
#     assert len(result.keys()) > 0

# def test_empty_collect():
#     result = runner(
#         ["--collect-only", os.fspath(TEST_DATA_PATH / "empty_discovery_pytest.py")]
#     )
#     # append to a file named "test.txt"
#     assert result is not None
#     assert result.get("tests") == empty_discovery_pytest_expected_output

# def test_simple_collect():
#     result = runner(
#         ["--collect-only", os.fspath(TEST_DATA_PATH / "simple_discovery_pytest.py")]
#     )
#     # append to a file named "test.txt"
#     assert result is not None
#     assert result.get("tests") == simple_discovery_pytest_expected_output


def test_empty_collect():
    result = runner(
        [
            "--collect-only",
            os.fspath(TEST_DATA_PATH / "unit_pytest_discovery_pytest.py"),
        ]
    )
    # append to a file named "test.txt"
    assert result is not None
    with open("test.py", "w") as f:
        for key, value in result.items():
            if key == "tests":
                f.write(f"{key}: {value}\n")

    assert result.get("tests") == unit_pytest_discovery_pytest_expected_output


# test UUIDs
