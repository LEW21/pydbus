from sys import version_info

from pydbus import xml_generator
from pydbus.generic import signal
from pydbus.strong_typing import typed_method, typed_property


@xml_generator.attach_introspection_xml
@xml_generator.interface("net.lvht.Foo1")
class Example(object):

	def __init__(self):
		self._rw = 42

	@typed_method(("s", ), "i")
	def OneParamReturn(self, parameter):
		return 42

	@typed_method(("s", ), None)
	def OneParamNoReturn(self, parameter):
		pass

	@typed_property("i")
	def ReadProperty(self):
		return 42

	@xml_generator.emits_changed_signal
	@typed_property("i")
	def RwProperty(self):
		return self._rw

	@RwProperty.setter
	def RwProperty(self, value):
		self._rw = value


@xml_generator.attach_introspection_xml
@xml_generator.interface("net.lvht.Foolback")
class MultiInterface(object):

	def MethodFoolback(self):
		pass

	@xml_generator.interface("net.lvht.Barface")
	def MethodBarface(self):
		pass

	@signal
	def SignalFoolback(self):
		pass

	@xml_generator.interface("net.lvht.Barface")
	@signal
	def SignalBarface(self):
		pass


def test_get_arguments():
	def nothing(self):
		pass

	def arguments(self, arg1, arg2):
		pass

	def ctx_argument(self, arg, dbus_context):
		pass

	@typed_method(tuple(), None)
	def typed_nothing(self):
		pass

	@typed_method(("s", "i"), None)
	def typed_arguments(self, arg1, arg2):
		pass

	assert xml_generator.get_arguments(nothing) == (tuple(), None)
	assert xml_generator.get_arguments(arguments) == ((("arg1", None), ("arg2", None)), None)
	assert xml_generator.get_arguments(ctx_argument) == ((("arg", None), ), None)

	assert xml_generator.get_arguments(typed_nothing) == (tuple(), None)
	assert xml_generator.get_arguments(typed_arguments) == ((("arg1", "s"), ("arg2", "i")), None)


def test_valid():
	assert not hasattr(Example.OneParamReturn, "dbus_interface")
	assert Example.OneParamReturn.arg_types == ("s", )
	assert Example.OneParamReturn.ret_type == "i"

	assert not hasattr(Example.OneParamNoReturn, "dbus_interface")
	assert Example.OneParamNoReturn.arg_types == ("s", )
	assert Example.OneParamNoReturn.ret_type is None

	assert not hasattr(Example.ReadProperty, "dbus_interface")
	assert isinstance(Example.ReadProperty, property)
	assert Example.ReadProperty.fget.prop_type == "i"
	assert Example.ReadProperty.fset is None

	assert not hasattr(Example.RwProperty, "dbus_interface")
	assert isinstance(Example.RwProperty, property)
	assert Example.RwProperty.fget.causes_signal is True
	assert Example.RwProperty.fget.prop_type == "i"
	assert Example.RwProperty.fset is not None

	assert Example.dbus == b'<node><interface name="net.lvht.Foo1"><method name="OneParamNoReturn"><arg direction="in" name="parameter" type="s" /></method><method name="OneParamReturn"><arg direction="in" name="parameter" type="s" /><arg direction="out" name="return" type="i" /></method><property access="read" name="ReadProperty" type="i" /><property access="readwrite" name="RwProperty" type="i"><annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true" /></property></interface></node>'


def test_multiple_interfaces():
	assert not hasattr(MultiInterface.MethodFoolback, "dbus_interface")
	assert MultiInterface.MethodBarface.dbus_interface == "net.lvht.Barface"
	assert not hasattr(MultiInterface.SignalFoolback, "dbus_interface")
	assert MultiInterface.SignalBarface.dbus_interface == "net.lvht.Barface"

	assert MultiInterface.dbus == b'<node><interface name="net.lvht.Barface"><method name="MethodBarface" /><signal name="SignalBarface" /></interface><interface name="net.lvht.Foolback"><method name="MethodFoolback" /><signal name="SignalFoolback" /></interface></node>'


def test_invalid_function():
	"""Test what happens if to many or to few types are defined in methods."""
	def Dummy(self, param=None):
		pass

	try:
		xml_generator.get_arguments(Dummy)
		assert False
	except ValueError as e:
		assert str(e) == "Default values are not allowed for method 'Dummy'"

	if version_info[0] == 2:
		E_NO_VARGS = (
			"Variable arguments arguments are not allowed for method 'Dummy'")
	else:
		E_NO_VARGS = E_NO_KWARGS = (
			"Variable arguments or keyword only arguments are not allowed for "
			"method 'Dummy'")

	def Dummy(self, *vargs):
		pass

	try:
		xml_generator.get_arguments(Dummy)
		assert False
	except ValueError as e:
		assert str(e) == E_NO_VARGS

	def Dummy(self, **kwargs):
		pass

	try:
		xml_generator.get_arguments(Dummy)
		assert False
	except ValueError as e:
		assert str(e) == E_NO_VARGS


def test_require_strong_typing():
	try:
		@xml_generator.attach_introspection_xml(True)
		@xml_generator.interface("net.lvht.Foo1")
		class Example(object):

			def Dummy(self, param):
				pass
	except ValueError as e:
		assert str(e) == "No argument types defined for method 'Dummy'"

	@xml_generator.attach_introspection_xml(True)
	@xml_generator.interface("net.lvht.Foo1")
	class RequiredExample(object):

		@typed_method(("s", ), None)
		def Dummy(self, param):
			pass

	assert RequiredExample.Dummy.arg_types == ("s", )
	assert RequiredExample.Dummy.ret_type is None

	@xml_generator.attach_introspection_xml(False)
	@xml_generator.interface("net.lvht.Foo1")
	class OptionalExample(object):

		@typed_method(("s", ), None)
		def Dummy(self, param):
			pass

	assert OptionalExample.dbus == RequiredExample.dbus
	assert OptionalExample is not RequiredExample


test_get_arguments()
test_valid()
test_multiple_interfaces()
test_invalid_function()
test_require_strong_typing()
