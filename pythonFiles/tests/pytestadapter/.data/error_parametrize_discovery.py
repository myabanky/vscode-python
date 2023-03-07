# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


import pytest


# This test is intentionally incorrect and is supposed to fail so that we can test the error handling.
@pytest.mark.parametrize("actual,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
def test_function():
    assert True
