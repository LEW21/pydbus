from gi.repository import GLib, Gio

class MethodCallFunc:
	__slots__ = ["object", "outargs"]

	def __init__(self, object, interfaces):
		self.object = object

		self.outargs = {}
		for iface in interfaces:
			for method in iface.methods:
				self.outargs[iface.name + "." + method.name] = [arg.signature for arg in method.out_args]

	def __call__(self, connection, sender, object_path, interface_name, method_name, parameters, invocation):
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

class GetPropertyFunc:
	def __init__(self, object, interfaces):
		self.object = object

		self.types = {}
		for iface in interfaces:
			for prop in iface.properties:
				self.types[iface.name + "." + prop.name] = prop.signature

	def __call__(self, connection, sender, object_path, interface_name, property_name):
		type = self.types[interface_name + "." + property_name]
		result = getattr(self.object, property_name)
		if "v" in type:
			# TODO
			return None
		return GLib.Variant(type, result)

class SetPropertyFunc:
	def __init__(self, object, interfaces):
		self.object = object

	def __call__(self, connection, sender, object_path, interface_name, property_name):
		setattr(self.object, property_name, value.unpack())

class ObjectRegistration(object):
	__slots__ = ("con", "ids")

	def __init__(self, con, path, interfaces, method_call_callback, get_property_callback, set_property_callback):
		self.con = con
		self.ids = [con.register_object(path, interface, method_call_callback, get_property_callback, set_property_callback) for interface in interfaces]

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

		for iface in interfaces:
			for signal in iface.signals:
				s_name = signal.name
				def EmitSignal(iface, signal):
					return lambda *args: self.con.emit_signal(None, path, iface.name, signal.name, GLib.Variant("(" + "".join(s.signature for s in signal.args) + ")", args))
				getattr(object, signal.name).connect(EmitSignal(iface, signal))

		if "org.freedesktop.DBus.Properties" not in (iface.name for iface in interfaces):
			if hasattr(object, "PropertiesChanged"):
				def onPropertiesChanged(iface, changed, invalidated):
					#args = GLib.Variant("(sa{sv}as)", (iface, changed, invalidated))
					# Crashes with TypeError: argument value: Expected GLib.Variant, but got int

					modified = list(changed.keys()) + invalidated
					args = GLib.Variant("(sa{sv}as)", (iface, {}, modified))
					self.con.emit_signal(None, path, "org.freedesktop.DBus.Properties", "PropertiesChanged", args)

				object.PropertiesChanged.connect(onPropertiesChanged)

		return ObjectRegistration(self.con, path, interfaces, MethodCallFunc(object, interfaces), GetPropertyFunc(object, interfaces), SetPropertyFunc(object, interfaces))
