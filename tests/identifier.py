from __future__ import print_function

import sys

from pydbus.identifier import filter_identifier


tests = [
	("abc", "abc"),
	("a_bC", "a_bC"),
	("a-b_c", "a_b_c"),
	("a@bc", "abc"),
	("!@#$%^&*", ""),
]

ret = 0
for inp, output in tests:
	if not filter_identifier(inp) == output:
		print("ERROR: filter(" + inp + ") returned: " + filter_identifier(input), file=sys.stderr)
		ret = 1

sys.exit(ret)
