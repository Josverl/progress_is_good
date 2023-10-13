import pytest

# only snippts tests
pytestmark = pytest.mark.snippets

def test_something():
    assert 1 == 1

def test_something_else():
    assert 1 == 2


@pytest.mark.parametrize("x", [1, 2, 3,4])
def test_alot(x):
    assert x <= 4
