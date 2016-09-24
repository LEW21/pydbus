from __future__ import print_function
import sys, traceback
from gi.repository import GLib, Gio
from . import generic
from .exitable import ExitableWithAliases
from functools import partial
from .method_call_context import MethodCallContext

try:
	from inspect import signature, Parameter
except:
	from ._inspect3 import signature, Parameter

class ObjectWrapper(ExitableWithAliases("unwrap")):
	__slots__ = ["object", "outargs", "property_types"]

	def __init__(self, object, interfaces):
		self.object = object

		self.outargs = {}
		for iface in interfaces:
			for method in iface.methods:
				self.outargs[iface.name + "." + method.name] = [arg.signature for arg in method.out_args]

		self.property_types = {}
		for iface in interfaces:
			for prop in iface.properties:
				self.property_types[iface.name + "." + prop.name] = prop.signature

		for iface in interfaces:
			for signal in iface.signals:
				s_name = signal.name
				def EmitSignal(iface, signal):
					return lambda *args: self.SignalEmitted(iface.name, signal.name, GLib.Variant("(" + "".join(s.signature for s in signal.args) + ")", args))
				self._at_exit(getattr(object, signal.name).connect(EmitSignal(iface, signal)).__exit__)

		if "org.freedesktop.DBus.Properties" not in (iface.name for iface in interfaces):
			try:
				def onPropertiesChanged(iface, changed, invalidated):
					changed = {key: GLib.Variant(self.property_types[iface + "." + key], val) for key, val in changed.items()}
					args = GLib.Variant("(sa{sv}as)", (iface, changed, invalidated))
					self.SignalEmitted("org.freedesktop.DBus.Properties", "PropertiesChanged", args)
				self._at_exit(object.PropertiesChanged.connect(onPropertiesChanged).__exit__)
			except AttributeError:
				pass

	SignalEmitted = generic.signal()

	def call_method(self, bus, connection, sender, object_path, interface_name, method_name, parameters, invocation):
		try:
			outargs = self.outargs[interface_name + "." + method_name]
			soutargs = "(" + "".join(outargs) + ")"

			method = getattr(self.object, method_name)

			sig = signature(method)

			kwargs = {}
			if "dbus_context" in sig.parameters and sig.parameters["dbus_context"].kind in (Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY):
				kwargs["dbus_context"] = MethodCallContext(bus, invocation)

			result = method(*parameters, **kwargs)

			if len(outargs) == 0:
				invocation.return_value(None)
			elif len(outargs) == 1:
				invocation.return_value(GLib.Variant(soutargs, (result,)))
			else:
				invocation.return_value(GLib.Variant(soutargs, result))

		except Exception as e:
			#TODO Think of a better way to translate Python exception types to DBus error types.
			e_type = type(e).__name__
			if not "." in e_type:
				e_type = "unknown." + e_type
			invocation.return_dbus_error(e_type, str(e))

	def get_property(self, connection, sender, object_path, interface_name, property_name):
		# Note: It's impossible to correctly return an exception, as
		# g_dbus_connection_register_object_with_closures does not support it
		try:
			type = self.property_types[interface_name + "." + property_name]
			result = getattr(self.object, property_name)
			return GLib.Variant(type, result)
		except Exception:
			print(traceback.format_exc(), file=sys.stderr)
			return None

	def set_property(self, connection, sender, object_path, interface_name, property_name, value):
		# Note: It's impossible to correctly return an exception, as
		# g_dbus_connection_register_object_with_closures does not support it
		try:
			type = self.property_types[interface_name + "." + property_name]
			assert(value.is_signature(type))
			setattr(self.object, property_name, value.unpack())
			return True
		except Exception:
			print(traceback.format_exc(), file=sys.stderr)
			return False

class ObjectRegistration(ExitableWithAliases("unregister")):
	__slots__ = ()

	def __init__(self, bus, path, interfaces, wrapper, own_wrapper=False):
		if own_wrapper:
			self._at_exit(wrapper.__exit__)

		def func(interface_name, signal_name, parameters):
			bus.con.emit_signal(None, path, interface_name, signal_name, parameters)

		self._at_exit(wrapper.SignalEmitted.connect(func).__exit__)

		try:
			ids = [bus.con.register_object(path, interface, partial(wrapper.call_method, bus), wrapper.get_property, wrapper.set_property) for interface in interfaces]
		except TypeError as e:
			if str(e).startswith("argument vtable: Expected Gio.DBusInterfaceVTable"):
				raise Exception("GLib 2.46 is required to publish objects; it is impossible in older versions.")
			else:
				raise

		self._at_exit(lambda: [bus.con.unregister_object(id) for id in ids])

class RegistrationMixin:
	__slots__ = ()

	def register_object(self, path, object, node_info):
		if node_info is None:
			try:
				node_info = type(object).dbus
			except AttributeError:
				node_info = type(object).__doc__

		if type(node_info) != list and type(node_info) != tuple:
			node_info = [node_info]

		node_info = [Gio.DBusNodeInfo.new_for_xml(ni) for ni in node_info]
		interfaces = sum((ni.interfaces for ni in node_info), [])

		wrapper = ObjectWrapper(object, interfaces)
		return ObjectRegistration(self, path, interfaces, wrapper, own_wrapper=True)
