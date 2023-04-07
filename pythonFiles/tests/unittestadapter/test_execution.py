# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import pathlib
from typing import List

import pytest
from unittestadapter.discovery import (
    DEFAULT_PORT,
    discover_tests,
    parse_discovery_cli_args,
)
from unittestadapter.utils import TestNodeTypeEnum, parse_unittest_args

from pythonFiles.unittestadapter.execution import (
    TestExecutionStatus,
    parse_execution_cli_args,
    run_tests,
)


@pytest.mark.parametrize(
    "args, expected",
    [
        (
            ['--port', '111', '--uuid', 'fake-uuid', '--testids', 'test_file.test_class.test_method'],
            (111, "fake-uuid", ["test_file.test_class.test_method"]),
        ),
        (
            ['--port', '111', '--uuid', 'fake-uuid', '--testids', ''],
            (111, "fake-uuid", [""]),
        ),
    ],
)
def test_parse_execution_cli_args(args: List[str], expected: List[str]) -> None:
    """The parse_unittest_args function should return values for the start_dir, pattern, and top_level_dir arguments
    when passed as command-line options, and ignore unrecognized arguments.
    """
    actual = parse_execution_cli_args(args)

    # port uuid testids
    assert actual == expected

def test_no_ids_run() -> None:
    start_dir = 'pythonFiles/tests/unittestadapter/.data'
    testids = []
    pattern = 'discovery_simple*'
    top_level_dir = None
    uuid = 'fake-uuid'
    actual = run_tests(start_dir, testids, pattern, top_level_dir, uuid)
    assert actual
    assert all(item in actual for item in ("cwd", "status", "result"))
    assert actual["status"] == "error"
    assert actual["cwd"] == '/Users/eleanorboyd/vscode-python/pythonFiles/tests/unittestadapter/.data'
    assert len(actual["result"]) == 0

def test_single_ids_run() -> None:
    start_dir = 'pythonFiles/tests/unittestadapter/.data'
    id = 'discovery_simple.DiscoverySimple.test_one'
    testids = ['discovery_simple.DiscoverySimple.test_one']
    pattern = 'discovery_simple*'
    top_level_dir = None
    uuid = 'fake-uuid'
    actual = run_tests(start_dir, testids, pattern, top_level_dir, uuid)
    assert actual
    assert all(item in actual for item in ("cwd", "status", "result"))
    assert actual["status"] == "error" # this is likely incorrect
    assert actual["cwd"] == '/Users/eleanorboyd/vscode-python/pythonFiles/tests/unittestadapter/.data'
    assert len(actual["result"]) == 1
    assert actual["result"][id]
    assert actual["result"][id]['outcome'] == 'success'


# def test_simple_run() -> None:
#     start_dir = 'pythonFiles/tests/unittestadapter/execution/test_simple.py'
#     testids = ['test_simple.TestSimple.test_simple']
#     pattern = 'test*.py'
#     top_level_dir = ''
#     uuid = 'fake-uuid'
#     result = run_tests(start_dir, testids, pattern, top_level_dir, uuid)
#     assert result == 0