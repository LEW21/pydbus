from pydbus.generic import signal
from pydbus.strong_typing import typed_method, typed_property


def test_signal():
	@signal
	@typed_method(("s", ), None)
	def dummy(self, parameter):
		pass

	assert hasattr(dummy, 'method')
	assert dummy.method.arg_types == ("s", )
	assert dummy.method.ret_type is None


def test_count_off():
	"""Test what happens if to many or to few types are defined in methods."""
	try:
		@typed_method(("s", "i", "o"), None)
		def dummy(self, parameter):
			pass

		assert False
	except ValueError as e:
		assert str(e) == "Number of argument types (3) differs from the number of parameters (1) in function 'dummy'"

	try:
		@typed_method(("s", "i"), "o")
		def dummy(self, parameter):
			pass

		assert False
	except ValueError as e:
		assert str(e) == "Number of argument types (2) differs from the number of parameters (1) in function 'dummy'"

	try:
		@typed_method(tuple(), None)
		def dummy(self, parameter):
			pass

		assert False
	except ValueError as e:
		assert str(e) == "Number of argument types (0) differs from the number of parameters (1) in function 'dummy'"


test_signal()
test_count_off()
