from gi.repository import GLib, Gio

from . import generic

class ObjectWrapper:
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
				getattr(object, signal.name).connect(EmitSignal(iface, signal))

		if "org.freedesktop.DBus.Properties" not in (iface.name for iface in interfaces):
			try:
				def onPropertiesChanged(iface, changed, invalidated):
					changed = {key: GLib.Variant(self.property_types[iface + "." + key], val) for key, val in changed.items()}
					args = GLib.Variant("(sa{sv}as)", (iface, changed, invalidated))
					self.SignalEmitted("org.freedesktop.DBus.Properties", "PropertiesChanged", args)
				object.PropertiesChanged.connect(onPropertiesChanged)
			except AttributeError:
				pass

	SignalEmitted = generic.signal()

	def call_method(self, connection, sender, object_path, interface_name, method_name, parameters, invocation):
		try:
			outargs = self.outargs[interface_name + "." + method_name]
			soutargs = "(" + "".join(outargs) + ")"

			method = getattr(self.object, method_name)

			result = method(*parameters)

			#if len(outargs) == 1:
			#	result = (result,)

			if len(outargs) == 0:
				invocation.return_value(None)
			else:
				invocation.return_value(GLib.Variant(soutargs, result))

		except Exception as e:
			#TODO Think of a better way to translate Python exception types to DBus error types.
			e_type = type(e).__name__
			if not "." in e_type:
				e_type = "unknown." + e_type
			invocation.return_dbus_error(e_type, str(e))

	def get_property(self, connection, sender, object_path, interface_name, property_name):
		type = self.property_types[interface_name + "." + property_name]
		result = getattr(self.object, property_name)
		return GLib.Variant(type, result)

	def set_property(self, connection, sender, object_path, interface_name, property_name, value):
		type = self.property_types[interface_name + "." + property_name]
		assert(value.is_signature(type))
		setattr(self.object, property_name, value.unpack())

class ObjectRegistration(object):
	__slots__ = ("con", "ids")

	def __init__(self, con, path, interfaces, wrapper):
		def func(interface_name, signal_name, parameters):
			con.emit_signal(None, path, interface_name, signal_name, parameters)
		wrapper.SignalEmitted.connect(func)

		self.con = con
		self.ids = [con.register_object(path, interface, wrapper.call_method, wrapper.get_property, wrapper.set_property) for interface in interfaces]

	def unregister(self):
		for id in self.ids:
			self.con.unregister_object(id)
		self.con = None
		self.ids = None

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		if not self.ids is None:
			self.unregister()

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
		return ObjectRegistration(self.con, path, interfaces, wrapper)
