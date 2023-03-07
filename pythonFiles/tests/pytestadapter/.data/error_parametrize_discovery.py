# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


import pytest


@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
def test_function():
    assert True
