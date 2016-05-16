from __future__ import print_function
import sys, traceback, inspect
from gi.repository import GLib, Gio
from . import generic
from .exitable import ExitableWithAliases

METHOD_IS_ASYNC = object()


class ObjectWrapper(ExitableWithAliases("unwrap")):
	__slots__ = ["object", "outargs", "property_types", "bus"]

	def __init__(self, object, interfaces, bus):
		self.object = object
		self.bus = bus

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

	def call_method(self, connection, sender, object_path, interface_name, method_name, parameters, invocation):
		def return_exception(exc):
			if isinstance(exc, GLib.GError):
				# the much simpler invocation.return_gerror(exc) raises TypeError.
				invocation.return_error_literal(GLib.quark_from_string(exc.domain), exc.code, exc.message)
			else:
				# TODO Think of a better way to translate Python exception types to DBus error types.
				e_type = type(exc).__name__
				if "." not in e_type:
					e_type = "unknown." + e_type
				invocation.return_dbus_error(e_type, str(exc))

		try:
			outargs = self.outargs[interface_name + "." + method_name]
			loutargs = len(outargs)
			soutargs = "(" + "".join(outargs) + ")"

			invocation.return_value_raw = return_value_raw = invocation.return_value

			def return_value(result):
				if loutargs == 0:
					return_value_raw(None)
				elif loutargs == 1:
					return_value_raw(GLib.Variant(soutargs, (result,)))
				else:
					return_value_raw(GLib.Variant(soutargs, result))
				return False

			invocation.return_value = return_value
			invocation.return_exception = return_exception

			method = getattr(self.object, method_name)
			is_async = getattr(method, "async", None)
			try:
				method_args = inspect.getargspec(method)[0]
			except TypeError:
				# not a function
				method_args = ()

			kw = {}
			if "dbus_bus" in method_args or getattr(method, "arg_dbus_bus", None):
				kw["dbus_bus"] = self.bus
			if "dbus_method_invocation" in method_args or getattr(method, "arg_dbus_bus", None) or is_async:
				kw["dbus_method_invocation"] = invocation

			result = method(*parameters, **kw)
			if not (is_async or result is METHOD_IS_ASYNC):
				return_value(result)

		except Exception as e:
			return_exception(e)

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

	def __init__(self, con, path, interfaces, wrapper, own_wrapper=False):
		if own_wrapper:
			self._at_exit(wrapper.__exit__)

		def func(interface_name, signal_name, parameters):
			con.emit_signal(None, path, interface_name, signal_name, parameters)

		self._at_exit(wrapper.SignalEmitted.connect(func).__exit__)

		ids = [con.register_object(path, interface, wrapper.call_method, wrapper.get_property, wrapper.set_property) for interface in interfaces]
		self._at_exit(lambda: [con.unregister_object(id) for id in ids])

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

		wrapper = ObjectWrapper(object, interfaces, self)
		return ObjectRegistration(self.con, path, interfaces, wrapper, own_wrapper=True)
