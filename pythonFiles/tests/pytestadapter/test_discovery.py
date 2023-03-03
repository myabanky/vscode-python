# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

from pytest import Config, MonkeyPatch, Session

from .helpers import TEST_DATA_PATH, runner

# def test_simple_collect():
#     result = runner(["--collect-only", os.fspath(TEST_DATA_PATH / "simple_discovery_pytest.py")])
#     assert result is not None
#     assert len(result.keys()) > 0


def test_empty_collect():
    result = runner(
        ["--collect-only", os.fspath(TEST_DATA_PATH / "empty_discovery_pytest.py")]
    )
    assert result is not None
    assert len(result.keys()) > 0


# test UUIDs
