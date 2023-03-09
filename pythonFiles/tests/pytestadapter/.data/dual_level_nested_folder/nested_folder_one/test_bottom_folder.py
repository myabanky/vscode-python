# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# This test id is dual_level_nested_folder/nested_folder_one/test_bottom_folder.py::test_bottom_function_t.
# This test passes.
def test_bottom_function_t():
    assert True

# This test id is dual_level_nested_folder/nested_folder_one/test_bottom_folder.py::test_bottom_function_f.
# This test fails.
def test_bottom_function_f():
    assert False
