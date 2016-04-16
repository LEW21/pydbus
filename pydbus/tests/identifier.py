from __future__ import print_function
from pydbus.identifier import filter_identifier
import sys

tests = [
	("abc", "abc"),
	("a_bC", "a_bC"),
	("a-b_c", "a_b_c"),
	("a@bc", "abc"),
	("!@#$%^&*", ""),
]

ret = 0
for input, output in tests:
	if not filter_identifier(input) == output:
		print("ERROR: filter(" + input + ") returned: " + filter_identifier(input), file=sys.stderr)
		ret = 1

sys.exit(ret)
