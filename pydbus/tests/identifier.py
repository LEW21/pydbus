import pytest

from pydbus.identifier import filter_identifier

@pytest.mark.parametrize("input, output", [
	("abc", "abc"),
	("a_bC", "a_bC"),
	("a-b_c", "a_b_c"),
	("a@bc", "abc"),
	("!@#$%^&*", ""),
])
def test_filter_identifier(input, output):
	assert filter_identifier(input) == output
