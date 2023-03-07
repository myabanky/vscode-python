import pytest


# Testing pytest with parametrized tests. The first two pass, the third fails.
@pytest.mark.parametrize("actual, expected", [("3+5", 8), ("2+4", 6), ("6+9", 16)])
def test_adding(actual, expected):
    assert eval(actual) == expected
