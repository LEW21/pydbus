from pydbus import xml_generator
from pydbus.generic import signal


@xml_generator.attach_introspection_xml
@xml_generator.interface("net.lvht.Foo1")
class Example(object):

	def __init__(self):
		self._rw = 42

	def OneParamReturn(self, parameter):
		return 42

	@xml_generator.emits_changed_signal
	@property
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

	assert xml_generator.get_arguments(nothing) == []
	assert xml_generator.get_arguments(arguments) == ["arg1", "arg2"]
	assert xml_generator.get_arguments(ctx_argument) == ["arg"]


def test_valid():
	assert not hasattr(Example.OneParamReturn, "dbus_interface")

	assert not hasattr(Example.RwProperty, "dbus_interface")
	assert isinstance(Example.RwProperty, property)
	assert Example.RwProperty.fget.causes_signal is True
	assert Example.RwProperty.fset is not None

	assert Example.dbus == b'<node><interface name="net.lvht.Foo1"><method name="OneParamReturn"><arg direction="in" name="parameter" /></method><property access="readwrite" name="RwProperty"><annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true" /></property></interface></node>'


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

	E_NO_VARGS = (
			"Variable arguments arguments are not allowed for method 'Dummy'")

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


test_get_arguments()
test_valid()
test_multiple_interfaces()
test_invalid_function()
